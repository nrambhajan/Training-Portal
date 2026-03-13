from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, SessionLocal
from models import Base, User
from auth import hash_password
import models  # noqa: F401 – ensure all models are registered

from routers import auth, modules, questions, trainees, attempts, dashboard, importer, microsoft_sso

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Linux Training Portal", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(modules.router)
app.include_router(questions.router)
app.include_router(trainees.router)
app.include_router(attempts.router)
app.include_router(dashboard.router)
app.include_router(importer.router)
app.include_router(microsoft_sso.router)


@app.on_event("startup")
def seed_admin():
    """Create default admin account if none exists."""
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.role == "admin").first():
            admin = User(
                username="admin",
                full_name="Trainer",
                password_hash=hash_password("admin123"),
                role="admin",
            )
            db.add(admin)
            db.commit()
            print("✅ Default admin created — username: admin / password: admin123")
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Linux Training Portal API"}
