from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload
from backend.app.database import get_db
from backend.app.models.user import User
from backend.app.models.fee import Fee
from backend.app.models.payment import Payment
from backend.app.models.student import Student
from backend.app.schemas.fee import (
    FeeCreate, FeeUpdate, FeeResponse,
    PaymentCreate, PaymentResponse, StudentFeeSummary
)
from backend.app.services.fee_service import fee_service
from backend.app.utils.permissions import require_roles, get_current_active_user
from backend.app.utils.helpers import log_audit_action

router = APIRouter(prefix="/fees", tags=["Fees"])

@router.get("", response_model=List[FeeResponse])
def list_fees(
    class_id: Optional[int] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    query = db.query(Fee).options(
        joinedload(Fee.class_obj),
        joinedload(Fee.academic_year)
    )
    if class_id:
        query = query.filter((Fee.class_id == class_id) | (Fee.class_id == None))

    fees = query.order_by(Fee.due_date.desc()).all()
    return [
        FeeResponse(
            id=f.id,
            title=f.title,
            fee_type=f.fee_type,
            class_id=f.class_id,
            academic_year_id=f.academic_year_id,
            amount=f.amount,
            due_date=f.due_date,
            description=f.description,
            class_name=f.class_obj.name if f.class_obj else "All Classes",
            academic_year_name=f.academic_year.name if f.academic_year else None,
            created_at=f.created_at
        )
        for f in fees
    ]

@router.post("", response_model=FeeResponse)
def create_fee(
    fee_in: FeeCreate,
    current_user: User = Depends(require_roles(["ADMIN"])),
    db: Session = Depends(get_db)
):
    fee = Fee(
        title=fee_in.title,
        fee_type=fee_in.fee_type,
        class_id=fee_in.class_id,
        academic_year_id=fee_in.academic_year_id,
        amount=fee_in.amount,
        due_date=fee_in.due_date,
        description=fee_in.description
    )
    db.add(fee)
    db.commit()
    db.refresh(fee)

    log_audit_action(db, "FEE_CREATE", "Fee", str(fee.id), f"Created fee {fee.title} ({fee.amount})", current_user.id)

    return FeeResponse(
        id=fee.id,
        title=fee.title,
        fee_type=fee.fee_type,
        class_id=fee.class_id,
        academic_year_id=fee.academic_year_id,
        amount=fee.amount,
        due_date=fee.due_date,
        description=fee.description,
        created_at=fee.created_at
    )

@router.delete("/{fee_id}")
def delete_fee(
    fee_id: int,
    current_user: User = Depends(require_roles(["ADMIN"])),
    db: Session = Depends(get_db)
):
    fee = db.query(Fee).filter(Fee.id == fee_id).first()
    if not fee:
        raise HTTPException(status_code=404, detail="Fee structure not found")
    db.delete(fee)
    db.commit()
    log_audit_action(db, "FEE_DELETE", "Fee", str(fee_id), "Deleted fee structure", current_user.id)
    return {"message": "Fee structure deleted successfully"}

# Payments
@router.post("/payments", response_model=PaymentResponse)
def record_payment(
    payment_in: PaymentCreate,
    current_user: User = Depends(require_roles(["ADMIN"])),
    db: Session = Depends(get_db)
):
    payment = fee_service.record_payment(db, payment_in)
    log_audit_action(db, "PAYMENT_RECORD", "Payment", str(payment.id), f"Payment of {payment.amount_paid} recorded for student {payment.student_id}", current_user.id)

    return PaymentResponse(
        id=payment.id,
        fee_id=payment.fee_id,
        student_id=payment.student_id,
        amount_paid=payment.amount_paid,
        payment_date=payment.payment_date,
        payment_method=payment.payment_method,
        payment_status=payment.payment_status,
        transaction_id=payment.transaction_id,
        remarks=payment.remarks,
        fee_title=payment.fee.title if payment.fee else None,
        student_name=payment.student.user.full_name if payment.student and payment.student.user else None,
        admission_number=payment.student.admission_number if payment.student else None,
        created_at=payment.created_at
    )

@router.get("/payments", response_model=List[PaymentResponse])
def list_payments(
    student_id: Optional[int] = None,
    fee_id: Optional[int] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    query = db.query(Payment).options(
        joinedload(Payment.fee),
        joinedload(Payment.student).joinedload(Student.user)
    )

    if current_user.role == "STUDENT" and current_user.student_profile:
        query = query.filter(Payment.student_id == current_user.student_profile.id)
    elif student_id:
        query = query.filter(Payment.student_id == student_id)

    if fee_id:
        query = query.filter(Payment.fee_id == fee_id)

    payments = query.order_by(Payment.payment_date.desc()).all()
    return [
        PaymentResponse(
            id=p.id,
            fee_id=p.fee_id,
            student_id=p.student_id,
            amount_paid=p.amount_paid,
            payment_date=p.payment_date,
            payment_method=p.payment_method,
            payment_status=p.payment_status,
            transaction_id=p.transaction_id,
            remarks=p.remarks,
            fee_title=p.fee.title if p.fee else None,
            student_name=p.student.user.full_name if p.student and p.student.user else None,
            admission_number=p.student.admission_number if p.student else None,
            created_at=p.created_at
        )
        for p in payments
    ]

@router.get("/student/{student_id}", response_model=StudentFeeSummary)
def get_student_fee_summary(
    student_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role == "STUDENT":
        if not current_user.student_profile or current_user.student_profile.id != student_id:
            raise HTTPException(status_code=403, detail="Can only view your own fee status")
    elif current_user.role == "PARENT":
        parent = current_user.parent_profile
        if not parent or not any(s.id == student_id for s in parent.students):
            raise HTTPException(status_code=403, detail="Can only view your child's fee status")

    return fee_service.get_student_fee_summary(db, student_id)
