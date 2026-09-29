from datetime import date, datetime
from typing import Optional, List, Any
from pydantic import BaseModel

# Department
class DepartmentBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentResponse(DepartmentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Academic Year
class AcademicYearBase(BaseModel):
    name: str
    start_date: date
    end_date: date
    is_current: bool = False

class AcademicYearCreate(AcademicYearBase):
    pass

class AcademicYearResponse(AcademicYearBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Section
class SectionBase(BaseModel):
    name: str
    class_id: int
    room_number: Optional[str] = None
    class_teacher_id: Optional[int] = None

class SectionCreate(SectionBase):
    pass

class SectionResponse(SectionBase):
    id: int
    class_name: Optional[str] = None
    class_teacher_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Class
class ClassBase(BaseModel):
    name: str
    grade_level: Optional[int] = None
    department_id: Optional[int] = None
    academic_year_id: Optional[int] = None

class ClassCreate(ClassBase):
    pass

class ClassResponse(ClassBase):
    id: int
    department_name: Optional[str] = None
    academic_year_name: Optional[str] = None
    sections: Optional[List[SectionResponse]] = []
    created_at: datetime

    class Config:
        from_attributes = True

# Subject
class SubjectBase(BaseModel):
    name: str
    code: str
    class_id: int
    teacher_id: Optional[int] = None

class SubjectCreate(SubjectBase):
    pass

class SubjectResponse(SubjectBase):
    id: int
    class_name: Optional[str] = None
    teacher_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Enrollment
class EnrollmentCreate(BaseModel):
    student_id: int
    class_id: int
    section_id: Optional[int] = None
    academic_year_id: int
    enrollment_date: Optional[date] = None
    status: Optional[str] = "active"

class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    class_id: int
    section_id: Optional[int] = None
    academic_year_id: int
    enrollment_date: date
    status: str
    student_name: Optional[str] = None
    class_name: Optional[str] = None
    section_name: Optional[str] = None
    academic_year_name: Optional[str] = None

    class Config:
        from_attributes = True

# Timetable
class TimetableBase(BaseModel):
    class_id: int
    section_id: int
    subject_id: int
    teacher_id: int
    day_of_week: str
    start_time: str
    end_time: str
    room_number: Optional[str] = None

class TimetableCreate(TimetableBase):
    pass

class TimetableResponse(TimetableBase):
    id: int
    class_name: Optional[str] = None
    section_name: Optional[str] = None
    subject_name: Optional[str] = None
    teacher_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
