from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from auth import get_current_user
from ssh_verifier import verify_task, check_output_match

router = APIRouter(tags=["attempts"])


def _get_latest_attempt(db: Session, user_id: int, question_id: int):
    return (
        db.query(models.Attempt)
        .filter(models.Attempt.user_id == user_id, models.Attempt.question_id == question_id)
        .order_by(models.Attempt.attempted_at.desc())
        .first()
    )


# ── Trainee: get questions for a module (with their attempt status) ───────────

@router.get("/my/modules", response_model=list[schemas.ModuleOut])
def my_modules(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    modules = db.query(models.Module).order_by(models.Module.created_at).all()
    result = []
    for m in modules:
        out = schemas.ModuleOut.model_validate(m)
        out.question_count = len(m.questions)
        result.append(out)
    return result


@router.get("/my/modules/{module_id}/questions")
def my_module_questions(
    module_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    module = db.query(models.Module).filter(models.Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    result = []
    for q in module.questions:
        attempt = _get_latest_attempt(db, current_user.id, q.id)
        result.append({
            "question": schemas.QuestionOutTrainee.model_validate(q),
            "attempt": schemas.AttemptOut.model_validate(attempt) if attempt else None,
        })
    return result


# ── Trainee: submit MCQ or output answer ─────────────────────────────────────

@router.post("/attempts/submit", response_model=schemas.AttemptOut)
def submit_answer(
    payload: schemas.AttemptSubmit,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    question = db.query(models.Question).filter(models.Question.id == payload.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    if question.type == "practical":
        raise HTTPException(status_code=400, detail="Use /attempts/verify for practical tasks")

    is_correct = False
    score = 0.0

    if question.type == "mcq":
        is_correct = str(payload.submitted_answer).strip() == str(question.correct_answer).strip()
        score = question.points if is_correct else 0.0

    elif question.type == "output":
        is_correct = check_output_match(
            submitted=payload.submitted_answer or "",
            verify_expected=question.verify_expected or "",
            verify_type=question.verify_type or "contains",
        )
        score = question.points if is_correct else 0.0

    elif question.type == "short_answer":
        # Auto-grade via keyword match if verify_expected is set, else leave pending for admin
        if question.verify_expected:
            is_correct = check_output_match(
                submitted=payload.submitted_answer or "",
                verify_expected=question.verify_expected or "",
                verify_type=question.verify_type or "contains",
            )
            score = question.points if is_correct else 0.0
        else:
            is_correct = None  # pending manual review
            score = None

    attempt = models.Attempt(
        user_id=current_user.id,
        question_id=question.id,
        submitted_answer=payload.submitted_answer,
        is_correct=is_correct,
        score=score,
        graded_at=datetime.utcnow(),
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return attempt


# ── Trainee: trigger SSH verification for practical tasks ────────────────────

@router.post("/attempts/verify/{question_id}", response_model=schemas.AttemptOut)
def verify_practical(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    if question.type != "practical":
        raise HTTPException(status_code=400, detail="This question is not a practical task")

    if not current_user.server_ip or not current_user.ssh_user or not current_user.ssh_password:
        raise HTTPException(
            status_code=400,
            detail="Server credentials not configured. Ask your trainer to update your profile.",
        )

    passed, output = verify_task(
        host=current_user.server_ip,
        port=current_user.ssh_port or 22,
        username=current_user.ssh_user,
        password=current_user.ssh_password,
        command=question.verify_command or "echo ok",
        verify_type=question.verify_type or "exit_code",
        verify_expected=question.verify_expected or "",
    )

    attempt = models.Attempt(
        user_id=current_user.id,
        question_id=question.id,
        submitted_answer="[SSH Verified]",
        server_output=output,
        is_correct=passed,
        score=question.points if passed else 0.0,
        graded_at=datetime.utcnow(),
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return attempt


# ── Trainee: my progress ──────────────────────────────────────────────────────

@router.get("/my/progress")
def my_progress(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    modules = db.query(models.Module).all()
    data = []
    for m in modules:
        total_pts = sum(q.points for q in m.questions)
        earned_pts = 0.0
        attempted = 0
        correct = 0
        for q in m.questions:
            att = _get_latest_attempt(db, current_user.id, q.id)
            if att:
                attempted += 1
                if att.is_correct:
                    correct += 1
                    earned_pts += att.score or 0
        data.append({
            "module_id": m.id,
            "module_title": m.title,
            "total_questions": len(m.questions),
            "attempted": attempted,
            "correct": correct,
            "score": earned_pts,
            "max_score": total_pts,
            "percent": round((earned_pts / total_pts * 100) if total_pts else 0, 1),
        })
    return data
