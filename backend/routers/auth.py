from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models, schemas, auth as auth_utils

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=schemas.TokenResponse)
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == payload.username).first()
    if not user or not auth_utils.verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = auth_utils.create_access_token({"sub": str(user.id), "role": user.role})
    return schemas.TokenResponse(
        access_token=token,
        role=user.role,
        full_name=user.full_name,
        user_id=user.id,
    )


@router.get("/me")
def me(current_user: models.User = Depends(auth_utils.get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "role": current_user.role,
        "full_name": current_user.full_name,
        "email": current_user.email,
    }
