from datetime import date, datetime
from typing import Optional, List, Any
from pydantic import BaseModel

class FeeBase(BaseModel):
    title: str
    fee_type: str = "Tuition"
    class_id: Optional[int] = None
    academic_year_id: Optional[int] = None
    amount: float
    due_date: date
    description: Optional[str] = None

class FeeCreate(FeeBase):
    pass

class FeeUpdate(BaseModel):
    title: Optional[str] = None
    fee_type: Optional[str] = None
    class_id: Optional[int] = None
    academic_year_id: Optional[int] = None
    amount: Optional[float] = None
    due_date: Optional[date] = None
    description: Optional[str] = None

class FeeResponse(FeeBase):
    id: int
    class_name: Optional[str] = None
    academic_year_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class PaymentCreate(BaseModel):
    fee_id: int
    student_id: int
    amount_paid: float
    payment_date: Optional[date] = None
    payment_method: str = "Cash"
    payment_status: str = "PAID"
    transaction_id: Optional[str] = None
    remarks: Optional[str] = None

class PaymentResponse(BaseModel):
    id: int
    fee_id: int
    student_id: int
    amount_paid: float
    payment_date: date
    payment_method: str
    payment_status: str
    transaction_id: Optional[str] = None
    remarks: Optional[str] = None
    fee_title: Optional[str] = None
    student_name: Optional[str] = None
    admission_number: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class StudentFeeItem(BaseModel):
    fee_id: int
    title: str
    fee_type: str
    total_amount: float
    amount_paid: float
    balance: float
    status: str
    due_date: date

class StudentFeeSummary(BaseModel):
    student_id: int
    student_name: str
    admission_number: str
    class_name: Optional[str] = None
    total_fees: float
    total_paid: float
    remaining_balance: float
    items: List[StudentFeeItem]
