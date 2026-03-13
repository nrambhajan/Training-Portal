from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from auth import require_admin

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/overview")
def overview(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin),
):
    trainees = db.query(models.User).filter(models.User.role == "trainee").all()
    modules = db.query(models.Module).all()
    all_questions = db.query(models.Question).all()
    total_questions = len(all_questions)

    result = []
    for trainee in trainees:
        earned = 0.0
        max_pts = sum(q.points for q in all_questions)
        correct = 0
        attempted = 0

        for q in all_questions:
            att = (
                db.query(models.Attempt)
                .filter(
                    models.Attempt.user_id == trainee.id,
                    models.Attempt.question_id == q.id,
                )
                .order_by(models.Attempt.attempted_at.desc())
                .first()
            )
            if att:
                attempted += 1
                if att.is_correct:
                    correct += 1
                    earned += att.score or 0

        result.append({
            "trainee_id": trainee.id,
            "trainee_name": trainee.full_name or trainee.username,
            "username": trainee.username,
            "server_ip": trainee.server_ip,
            "total_questions": total_questions,
            "attempted": attempted,
            "correct": correct,
            "score": round(earned, 2),
            "max_score": round(max_pts, 2),
            "percent": round((earned / max_pts * 100) if max_pts else 0, 1),
        })

    return {
        "trainees": result,
        "total_modules": len(modules),
        "total_questions": total_questions,
        "total_trainees": len(trainees),
    }


@router.get("/trainee/{trainee_id}")
def trainee_detail(
    trainee_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin),
):
    trainee = db.query(models.User).filter(
        models.User.id == trainee_id, models.User.role == "trainee"
    ).first()
    if not trainee:
        return {"error": "Trainee not found"}

    modules = db.query(models.Module).all()
    module_data = []

    for m in modules:
        questions_data = []
        for q in m.questions:
            att = (
                db.query(models.Attempt)
                .filter(
                    models.Attempt.user_id == trainee_id,
                    models.Attempt.question_id == q.id,
                )
                .order_by(models.Attempt.attempted_at.desc())
                .first()
            )
            questions_data.append({
                "question_id": q.id,
                "type": q.type,
                "text": q.text,
                "points": q.points,
                "correct_answer": q.correct_answer,
                "attempt": {
                    "id": att.id,
                    "submitted_answer": att.submitted_answer,
                    "server_output": att.server_output,
                    "is_correct": att.is_correct,
                    "score": att.score,
                    "attempted_at": att.attempted_at.isoformat(),
                    "graded_at": att.graded_at.isoformat() if att.graded_at else None,
                } if att else None,
            })
        module_data.append({
            "module_id": m.id,
            "module_title": m.title,
            "questions": questions_data,
        })

    return {
        "trainee": {
            "id": trainee.id,
            "username": trainee.username,
            "full_name": trainee.full_name,
            "server_ip": trainee.server_ip,
        },
        "modules": module_data,
    }


@router.put("/grade/{attempt_id}")
def grade_attempt(
    attempt_id: int,
    payload: schemas.GradeAttempt,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin),
):
    attempt = db.query(models.Attempt).filter(models.Attempt.id == attempt_id).first()
    if not attempt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attempt not found")

    question = db.query(models.Question).filter(models.Question.id == attempt.question_id).first()

    attempt.is_correct = payload.is_correct
    attempt.score = question.points if payload.is_correct else 0.0
    attempt.graded_at = datetime.utcnow()
    db.commit()
    db.refresh(attempt)

    return {
        "id": attempt.id,
        "is_correct": attempt.is_correct,
        "score": attempt.score,
        "graded_at": attempt.graded_at.isoformat(),
    }
