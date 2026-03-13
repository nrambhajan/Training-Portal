from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from auth import require_admin, get_current_user

router = APIRouter(tags=["questions"])


@router.get("/modules/{module_id}/questions", response_model=list[schemas.QuestionOut])
def list_questions(
    module_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin),
):
    module = db.query(models.Module).filter(models.Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return module.questions


@router.post("/modules/{module_id}/questions", response_model=schemas.QuestionOut)
def create_question(
    module_id: int,
    payload: schemas.QuestionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin),
):
    module = db.query(models.Module).filter(models.Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    q = models.Question(module_id=module_id, **payload.model_dump())
    db.add(q)
    db.commit()
    db.refresh(q)
    return q


@router.put("/questions/{question_id}", response_model=schemas.QuestionOut)
def update_question(
    question_id: int,
    payload: schemas.QuestionUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin),
):
    q = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    for k, v in payload.model_dump(exclude_none=True).items():
        setattr(q, k, v)
    db.commit()
    db.refresh(q)
    return q


@router.delete("/questions/{question_id}")
def delete_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin),
):
    q = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    db.delete(q)
    db.commit()
    return {"ok": True}
