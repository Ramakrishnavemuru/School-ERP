from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False, index=True)  # ADMIN, PRINCIPAL, TEACHER, STUDENT, PARENT
    is_active = Column(Boolean, default=True, nullable=False)
    phone = Column(String(20), nullable=True)
    avatar = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    student_profile = relationship("Student", back_populates="user", uselist=False, cascade="all, delete-orphan")
    teacher_profile = relationship("Teacher", back_populates="user", uselist=False, cascade="all, delete-orphan")
    parent_profile = relationship("Parent", back_populates="user", uselist=False, cascade="all, delete-orphan")
    principal_profile = relationship("Principal", back_populates="user", uselist=False, cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="user", cascade="all, delete-orphan")
    leaves = relationship("Leave", back_populates="user", foreign_keys="Leave.user_id", cascade="all, delete-orphan")
    complaints = relationship("Complaint", back_populates="user", foreign_keys="Complaint.user_id", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user")
