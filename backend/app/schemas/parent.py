from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, EmailStr
from backend.app.schemas.user import UserResponse

class ParentBase(BaseModel):
    occupation: Optional[str] = None
    relation_type: Optional[str] = "Guardian"
    address: Optional[str] = None
    emergency_contact: Optional[str] = None

class ParentCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: str
    phone: Optional[str] = None
    occupation: Optional[str] = None
    relation_type: Optional[str] = "Guardian"
    address: Optional[str] = None
    emergency_contact: Optional[str] = None

class ParentUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    occupation: Optional[str] = None
    relation_type: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None

class ParentResponse(BaseModel):
    id: int
    user_id: int
    occupation: Optional[str] = None
    relation_type: Optional[str] = "Guardian"
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    user: Optional[UserResponse] = None
    students: Optional[List[Any]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
