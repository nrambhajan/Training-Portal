from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from auth import require_admin, hash_password

router = APIRouter(prefix="/trainees", tags=["trainees"])


@router.get("", response_model=list[schemas.TraineeOut])
def list_trainees(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin),
):
    return db.query(models.User).filter(models.User.role == "trainee").all()


@router.post("", response_model=schemas.TraineeOut)
def create_trainee(
    payload: schemas.TraineeCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin),
):
    if db.query(models.User).filter(models.User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    data = payload.model_dump()
    raw_password = data.pop("password")
    trainee = models.User(
        **data,
        password_hash=hash_password(raw_password),
        role="trainee",
    )
    db.add(trainee)
    db.commit()
    db.refresh(trainee)
    return trainee


@router.put("/{trainee_id}", response_model=schemas.TraineeOut)
def update_trainee(
    trainee_id: int,
    payload: schemas.TraineeUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin),
):
    trainee = db.query(models.User).filter(
        models.User.id == trainee_id, models.User.role == "trainee"
    ).first()
    if not trainee:
        raise HTTPException(status_code=404, detail="Trainee not found")

    data = payload.model_dump(exclude_none=True)
    if "password" in data:
        trainee.password_hash = hash_password(data.pop("password"))
    for k, v in data.items():
        setattr(trainee, k, v)
    db.commit()
    db.refresh(trainee)
    return trainee


@router.delete("/{trainee_id}")
def delete_trainee(
    trainee_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin),
):
    trainee = db.query(models.User).filter(
        models.User.id == trainee_id, models.User.role == "trainee"
    ).first()
    if not trainee:
        raise HTTPException(status_code=404, detail="Trainee not found")
    db.delete(trainee)
    db.commit()
    return {"ok": True}
