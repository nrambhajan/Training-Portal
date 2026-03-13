from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(10), nullable=False, default="trainee")  # admin | trainee
    full_name = Column(String(100), nullable=True)
    # Server credentials (trainees only)
    server_ip = Column(String(50), nullable=True)
    ssh_user = Column(String(50), nullable=True)
    ssh_password = Column(String(255), nullable=True)
    ssh_port = Column(Integer, nullable=True, default=22)
    created_at = Column(DateTime, default=datetime.utcnow)

    attempts = relationship("Attempt", back_populates="user", cascade="all, delete-orphan")


class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    questions = relationship("Question", back_populates="module", cascade="all, delete-orphan",
                             order_by="Question.order")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    # mcq | practical | output
    type = Column(String(20), nullable=False)
    text = Column(Text, nullable=False)
    # MCQ: list of option strings
    options = Column(JSON, nullable=True)
    # MCQ: correct option index (0-based); output: expected pattern; practical: not used
    correct_answer = Column(Text, nullable=True)
    # Practical / output verification
    verify_command = Column(Text, nullable=True)  # command run on server (practical only)
    verify_expected = Column(Text, nullable=True)  # expected output string or regex
    # exit_code | contains | regex
    verify_type = Column(String(20), nullable=True, default="exit_code")
    points = Column(Float, nullable=False, default=1.0)
    order = Column(Integer, nullable=False, default=0)
    hint = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    module = relationship("Module", back_populates="questions")
    attempts = relationship("Attempt", back_populates="question", cascade="all, delete-orphan")


class Attempt(Base):
    __tablename__ = "attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    submitted_answer = Column(Text, nullable=True)
    server_output = Column(Text, nullable=True)
    is_correct = Column(Boolean, nullable=True)  # None = not yet graded
    score = Column(Float, nullable=True)
    attempted_at = Column(DateTime, default=datetime.utcnow)
    graded_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="attempts")
    question = relationship("Question", back_populates="attempts")
