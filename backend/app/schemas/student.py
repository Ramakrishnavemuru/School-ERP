from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from backend.app.schemas.user import UserResponse

class StudentBase(BaseModel):
    admission_number: str
    roll_number: Optional[str] = None
    class_id: Optional[int] = None
    section_id: Optional[int] = None
    parent_id: Optional[int] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    blood_group: Optional[str] = None
    admission_date: Optional[date] = None
    address: Optional[str] = None

class StudentCreate(BaseModel):
    # User info
    username: str
    email: EmailStr
    password: str
    full_name: str
    phone: Optional[str] = None
    # Student info
    admission_number: str
    roll_number: Optional[str] = None
    class_id: Optional[int] = None
    section_id: Optional[int] = None
    parent_id: Optional[int] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    blood_group: Optional[str] = None
    admission_date: Optional[date] = None
    address: Optional[str] = None

class StudentUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    admission_number: Optional[str] = None
    roll_number: Optional[str] = None
    class_id: Optional[int] = None
    section_id: Optional[int] = None
    parent_id: Optional[int] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    blood_group: Optional[str] = None
    address: Optional[str] = None

class StudentResponse(BaseModel):
    id: int
    user_id: int
    admission_number: str
    roll_number: Optional[str] = None
    class_id: Optional[int] = None
    section_id: Optional[int] = None
    parent_id: Optional[int] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    blood_group: Optional[str] = None
    admission_date: Optional[date] = None
    address: Optional[str] = None
    user: Optional[UserResponse] = None
    class_name: Optional[str] = None
    section_name: Optional[str] = None
    parent_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
