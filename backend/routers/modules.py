from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from auth import require_admin, get_current_user

router = APIRouter(prefix="/modules", tags=["modules"])


@router.get("", response_model=list[schemas.ModuleOut])
def list_modules(
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


@router.post("", response_model=schemas.ModuleOut)
def create_module(
    payload: schemas.ModuleCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin),
):
    module = models.Module(**payload.model_dump())
    db.add(module)
    db.commit()
    db.refresh(module)
    out = schemas.ModuleOut.model_validate(module)
    out.question_count = 0
    return out


@router.put("/{module_id}", response_model=schemas.ModuleOut)
def update_module(
    module_id: int,
    payload: schemas.ModuleUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin),
):
    module = db.query(models.Module).filter(models.Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    for k, v in payload.model_dump(exclude_none=True).items():
        setattr(module, k, v)
    db.commit()
    db.refresh(module)
    out = schemas.ModuleOut.model_validate(module)
    out.question_count = len(module.questions)
    return out


@router.delete("/{module_id}")
def delete_module(
    module_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin),
):
    module = db.query(models.Module).filter(models.Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    db.delete(module)
    db.commit()
    return {"ok": True}
