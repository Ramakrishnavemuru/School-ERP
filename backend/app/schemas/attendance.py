from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel

class AttendanceRecord(BaseModel):
    student_id: int
    status: str  # Present, Absent, Late, Excused
    remarks: Optional[str] = None

class AttendanceBulkCreate(BaseModel):
    class_id: int
    section_id: int
    date: date
    records: List[AttendanceRecord]

class AttendanceCreate(BaseModel):
    student_id: int
    class_id: int
    section_id: int
    date: date
    status: str
    remarks: Optional[str] = None

class AttendanceUpdate(BaseModel):
    status: str
    remarks: Optional[str] = None

class AttendanceResponse(BaseModel):
    id: int
    student_id: int
    class_id: int
    section_id: int
    date: date
    status: str
    remarks: Optional[str] = None
    recorded_by: Optional[int] = None
    student_name: Optional[str] = None
    admission_number: Optional[str] = None
    roll_number: Optional[str] = None
    class_name: Optional[str] = None
    section_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class AttendanceStats(BaseModel):
    total_days: int
    present_days: int
    absent_days: int
    late_days: int
    excused_days: int
    percentage: float
