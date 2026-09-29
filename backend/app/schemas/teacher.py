from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from backend.app.schemas.user import UserResponse

class TeacherBase(BaseModel):
    employee_id: str
    department_id: Optional[int] = None
    qualification: Optional[str] = None
    designation: Optional[str] = "Teacher"
    joining_date: Optional[date] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class TeacherCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: str
    employee_id: str
    department_id: Optional[int] = None
    qualification: Optional[str] = None
    designation: Optional[str] = "Teacher"
    joining_date: Optional[date] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class TeacherUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    department_id: Optional[int] = None
    qualification: Optional[str] = None
    designation: Optional[str] = None
    address: Optional[str] = None

class TeacherResponse(BaseModel):
    id: int
    user_id: int
    employee_id: str
    department_id: Optional[int] = None
    qualification: Optional[str] = None
    designation: Optional[str] = None
    joining_date: Optional[date] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    user: Optional[UserResponse] = None
    department_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
