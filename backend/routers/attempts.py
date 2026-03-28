from datetime import datetime
import random
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


def _count_attempts(db: Session, user_id: int, question_id: int) -> int:
    return (
        db.query(models.Attempt)
        .filter(models.Attempt.user_id == user_id, models.Attempt.question_id == question_id)
        .count()
    )


def _module_percent(db: Session, user_id: int, module: models.Module) -> float:
    """Calculate user's score percent in a module."""
    max_pts = sum(q.points for q in module.questions)
    if max_pts == 0:
        return 100.0
    earned = 0.0
    for q in module.questions:
        att = _get_latest_attempt(db, user_id, q.id)
        if att and att.is_correct:
            earned += att.score or 0
    return round((earned / max_pts * 100), 1)


# ── Trainee: list modules ──────────────────────────────────────────────────────

@router.get("/my/modules", response_model=list[schemas.ModuleOut])
def my_modules(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    # Trainees only see published modules; admin sees all
    query = db.query(models.Module).order_by(models.Module.sort_order, models.Module.id)
    if current_user.role == "trainee":
        query = query.filter(models.Module.is_published == True)
    modules = query.all()
    result = []
    for m in modules:
        out = schemas.ModuleOut.model_validate(m)
        out.question_count = len(m.questions)
        result.append(out)
    return result


# ── Module unlock status ──────────────────────────────────────────────────────

@router.get("/my/modules/unlock-status")
def my_unlock_status(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    query = db.query(models.Module).order_by(models.Module.sort_order, models.Module.id)
    if current_user.role == "trainee":
        query = query.filter(models.Module.is_published == True)
    modules = query.all()
    result = []
    for idx, m in enumerate(modules):
        locked = False
        required_pct = 0
        prev_pct = 0
        if m.unlock_percent and m.unlock_percent > 0 and idx > 0:
            prev_module = modules[idx - 1]
            prev_pct = _module_percent(db, current_user.id, prev_module)
            required_pct = m.unlock_percent
            if prev_pct < m.unlock_percent:
                locked = True
        result.append({
            "module_id": m.id,
            "locked": locked,
            "required_pct": required_pct,
            "prev_pct": prev_pct,
        })
    return result


# ── Trainee: get questions for a module ───────────────────────────────────────

@router.get("/my/modules/{module_id}/questions")
def my_module_questions(
    module_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    module = db.query(models.Module).filter(models.Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    # Block trainees from accessing unpublished modules
    if current_user.role == "trainee" and not module.is_published:
        raise HTTPException(status_code=403, detail="This module is not available yet.")

    # Check unlock
    modules = db.query(models.Module).order_by(models.Module.sort_order, models.Module.id).all()
    for idx, m in enumerate(modules):
        if m.id == module_id and m.unlock_percent and m.unlock_percent > 0 and idx > 0:
            prev_module = modules[idx - 1]
            prev_pct = _module_percent(db, current_user.id, prev_module)
            if prev_pct < m.unlock_percent:
                raise HTTPException(
                    status_code=403,
                    detail=f"Complete the previous module with at least {int(m.unlock_percent)}% to unlock this one."
                )
            break

    # Randomize question order per trainee (consistent seed so order stays same on reload)
    questions = list(module.questions)
    rng = random.Random(current_user.id * 1000 + module_id)
    rng.shuffle(questions)

    result = []
    for q in questions:
        attempt = _get_latest_attempt(db, current_user.id, q.id)
        attempt_count = _count_attempts(db, current_user.id, q.id)
        q_out = schemas.QuestionOutTrainee.model_validate(q)
        att_out = schemas.AttemptOut.model_validate(attempt) if attempt else None

        result.append({
            "question": q_out,
            "attempt": att_out,
            "attempt_count": attempt_count,
        })
    return result


# ── Trainee: submit answer ────────────────────────────────────────────────────

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

    # Check max attempts
    if question.max_attempts:
        count = _count_attempts(db, current_user.id, question.id)
        if count >= question.max_attempts:
            raise HTTPException(
                status_code=400,
                detail=f"Maximum attempts ({question.max_attempts}) reached for this question."
            )

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
        graded_at=datetime.utcnow() if is_correct is not None else None,
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return attempt


# ── Trainee: SSH verification for practical tasks ────────────────────────────

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
    query = db.query(models.Module).order_by(models.Module.sort_order, models.Module.id)
    if current_user.role == "trainee":
        query = query.filter(models.Module.is_published == True)
    modules = query.all()
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
