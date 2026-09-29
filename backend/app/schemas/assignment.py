from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class AssignmentBase(BaseModel):
    title: str
    description: Optional[str] = None
    class_id: int
    section_id: Optional[int] = None
    subject_id: int
    due_date: datetime
    max_marks: float = 100.0

class AssignmentCreate(AssignmentBase):
    pass

class AssignmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    max_marks: Optional[float] = None
    section_id: Optional[int] = None

class AssignmentResponse(AssignmentBase):
    id: int
    teacher_id: int
    attachment_path: Optional[str] = None
    class_name: Optional[str] = None
    section_name: Optional[str] = None
    subject_name: Optional[str] = None
    teacher_name: Optional[str] = None
    submission_count: Optional[int] = 0
    my_submission: Optional[dict] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SubmissionGrade(BaseModel):
    marks_obtained: float
    feedback: Optional[str] = None

class SubmissionResponse(BaseModel):
    id: int
    assignment_id: int
    student_id: int
    student_name: Optional[str] = None
    admission_number: Optional[str] = None
    file_path: str
    submission_date: datetime
    marks_obtained: Optional[float] = None
    feedback: Optional[str] = None
    status: str
    assignment_title: Optional[str] = None
    max_marks: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True

class StudyMaterialCreate(BaseModel):
    title: str
    description: Optional[str] = None
    class_id: int
    subject_id: int

class StudyMaterialResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    class_id: int
    subject_id: int
    teacher_id: int
    file_path: str
    file_type: Optional[str] = None
    file_size: Optional[int] = None
    upload_date: datetime
    class_name: Optional[str] = None
    subject_name: Optional[str] = None
    teacher_name: Optional[str] = None

    class Config:
        from_attributes = True
