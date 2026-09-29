from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class ResultItem(BaseModel):
    student_id: int
    marks_obtained: float
    max_marks: float = 100.0
    remarks: Optional[str] = None

class ResultBulkCreate(BaseModel):
    exam_id: int
    subject_id: int
    records: List[ResultItem]

class ResultCreate(BaseModel):
    exam_id: int
    student_id: int
    subject_id: int
    marks_obtained: float
    max_marks: float = 100.0
    remarks: Optional[str] = None

class ResultUpdate(BaseModel):
    marks_obtained: float
    max_marks: Optional[float] = 100.0
    remarks: Optional[str] = None

class ResultResponse(BaseModel):
    id: int
    exam_id: int
    student_id: int
    subject_id: int
    marks_obtained: float
    max_marks: float
    percentage: Optional[float] = None
    grade: Optional[str] = None
    remarks: Optional[str] = None
    exam_name: Optional[str] = None
    student_name: Optional[str] = None
    admission_number: Optional[str] = None
    roll_number: Optional[str] = None
    subject_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class StudentReportCard(BaseModel):
    exam_id: int
    exam_name: str
    student_id: int
    student_name: str
    admission_number: str
    class_name: Optional[str] = None
    section_name: Optional[str] = None
    results: List[ResultResponse]
    total_obtained: float
    total_max: float
    percentage: float
    grade: str
