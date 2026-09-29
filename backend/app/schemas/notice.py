from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class NoticeBase(BaseModel):
    title: str
    content: str
    target_role: str = "ALL"  # ALL, STUDENT, TEACHER, PARENT
    is_published: bool = True
    expires_at: Optional[datetime] = None

class NoticeCreate(NoticeBase):
    pass

class NoticeUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    target_role: Optional[str] = None
    is_published: Optional[bool] = None
    expires_at: Optional[datetime] = None

class NoticeResponse(NoticeBase):
    id: int
    published_by: int
    publish_date: datetime
    publisher_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
