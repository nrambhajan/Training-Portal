from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel


# ── Auth ────────────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    full_name: Optional[str]
    user_id: int


# ── Users / Trainees ─────────────────────────────────────────────────────────

class TraineeCreate(BaseModel):
    username: str
    password: str
    full_name: Optional[str] = None
    email: Optional[str] = None
    server_ip: Optional[str] = None
    ssh_user: Optional[str] = None
    ssh_password: Optional[str] = None
    ssh_port: int = 22


class TraineeUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    server_ip: Optional[str] = None
    ssh_user: Optional[str] = None
    ssh_password: Optional[str] = None
    ssh_port: Optional[int] = None
    password: Optional[str] = None


class TraineeOut(BaseModel):
    id: int
    username: str
    full_name: Optional[str]
    email: Optional[str]
    server_ip: Optional[str]
    ssh_user: Optional[str]
    ssh_port: Optional[int]
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Modules ──────────────────────────────────────────────────────────────────

class ModuleCreate(BaseModel):
    title: str
    description: Optional[str] = None


class ModuleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class ModuleOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    created_at: datetime
    question_count: int = 0

    model_config = {"from_attributes": True}


# ── Questions ────────────────────────────────────────────────────────────────

class QuestionCreate(BaseModel):
    type: str  # mcq | practical | output
    text: str
    options: Optional[List[str]] = None
    correct_answer: Optional[str] = None
    verify_command: Optional[str] = None
    verify_expected: Optional[str] = None
    verify_type: Optional[str] = "exit_code"  # exit_code | contains | regex
    points: float = 1.0
    order: int = 0
    hint: Optional[str] = None


class QuestionUpdate(BaseModel):
    type: Optional[str] = None
    text: Optional[str] = None
    options: Optional[List[str]] = None
    correct_answer: Optional[str] = None
    verify_command: Optional[str] = None
    verify_expected: Optional[str] = None
    verify_type: Optional[str] = None
    points: Optional[float] = None
    order: Optional[int] = None
    hint: Optional[str] = None


class QuestionOut(BaseModel):
    id: int
    module_id: int
    type: str
    text: str
    options: Optional[List[str]]
    correct_answer: Optional[str]
    verify_command: Optional[str]
    verify_expected: Optional[str]
    verify_type: Optional[str]
    points: float
    order: int
    hint: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


# Trainee-facing question (hides correct answer)
class QuestionOutTrainee(BaseModel):
    id: int
    module_id: int
    type: str
    text: str
    options: Optional[List[str]]
    points: float
    order: int
    hint: Optional[str]

    model_config = {"from_attributes": True}


# ── Attempts ─────────────────────────────────────────────────────────────────

class AttemptSubmit(BaseModel):
    question_id: int
    submitted_answer: Optional[str] = None


class AttemptOut(BaseModel):
    id: int
    question_id: int
    submitted_answer: Optional[str]
    server_output: Optional[str]
    is_correct: Optional[bool]
    score: Optional[float]
    attempted_at: datetime
    graded_at: Optional[datetime]

    model_config = {"from_attributes": True}


# ── Dashboard / Results ───────────────────────────────────────────────────────

class TraineeProgress(BaseModel):
    trainee: TraineeOut
    total_questions: int
    attempted: int
    correct: int
    score: float
    max_score: float
    percent: float


class QuestionResult(BaseModel):
    question: QuestionOut
    attempt: Optional[AttemptOut]


# ── Grading ──────────────────────────────────────────────────────────────────

class GradeAttempt(BaseModel):
    is_correct: bool
