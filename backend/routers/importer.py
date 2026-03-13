from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth import require_admin
import models
from csv_importer import import_csv_to_db

router = APIRouter(prefix="/import", tags=["import"])


@router.post("/csv")
async def import_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin),
):
    if not file.filename.endswith((".csv", ".CSV")):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted")

    content_bytes = await file.read()
    # Try UTF-8 first, fall back to latin-1 (common for Excel exports)
    try:
        content = content_bytes.decode("utf-8-sig")
    except UnicodeDecodeError:
        content = content_bytes.decode("latin-1")

    result = import_csv_to_db(content, db)
    return result
