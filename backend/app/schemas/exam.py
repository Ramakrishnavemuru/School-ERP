from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel

class ExamBase(BaseModel):
    name: str
    exam_type: str  # Midterm, Final, Unit Test, Quiz
    academic_year_id: Optional[int] = None
    class_id: Optional[int] = None
    start_date: date
    end_date: date
    is_published: bool = False

class ExamCreate(ExamBase):
    pass

class ExamUpdate(BaseModel):
    name: Optional[str] = None
    exam_type: Optional[str] = None
    academic_year_id: Optional[int] = None
    class_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_published: Optional[bool] = None

class ExamResponse(ExamBase):
    id: int
    academic_year_name: Optional[str] = None
    class_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
