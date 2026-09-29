from datetime import date
from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from backend.app.models.fee import Fee
from backend.app.models.payment import Payment
from backend.app.models.student import Student
from backend.app.schemas.fee import PaymentCreate, StudentFeeSummary, StudentFeeItem

class FeeService:
    @staticmethod
    def record_payment(db: Session, payment_in: PaymentCreate) -> Payment:
        fee = db.query(Fee).filter(Fee.id == payment_in.fee_id).first()
        if not fee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fee structure not found"
            )

        student = db.query(Student).filter(Student.id == payment_in.student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )

        payment = Payment(
            fee_id=payment_in.fee_id,
            student_id=payment_in.student_id,
            amount_paid=payment_in.amount_paid,
            payment_date=payment_in.payment_date or date.today(),
            payment_method=payment_in.payment_method,
            payment_status=payment_in.payment_status,
            transaction_id=payment_in.transaction_id,
            remarks=payment_in.remarks
        )
        db.add(payment)
        db.commit()
        db.refresh(payment)
        return payment

    @staticmethod
    def get_student_fee_summary(db: Session, student_id: int) -> StudentFeeSummary:
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )

        # Get all fees for this student's class or global fees (class_id IS NULL)
        fees = db.query(Fee).filter(
            (Fee.class_id == student.class_id) | (Fee.class_id == None)
        ).all()

        items: List[StudentFeeItem] = []
        total_fees = 0.0
        total_paid = 0.0

        for fee in fees:
            payments = db.query(Payment).filter(
                Payment.fee_id == fee.id,
                Payment.student_id == student_id
            ).all()
            paid_amount = sum(p.amount_paid for p in payments)
            balance = max(0.0, fee.amount - paid_amount)

            if paid_amount >= fee.amount:
                pay_status = "PAID"
            elif paid_amount > 0:
                pay_status = "PARTIAL"
            else:
                pay_status = "UNPAID"

            total_fees += fee.amount
            total_paid += paid_amount

            items.append(StudentFeeItem(
                fee_id=fee.id,
                title=fee.title,
                fee_type=fee.fee_type,
                total_amount=fee.amount,
                amount_paid=paid_amount,
                balance=balance,
                status=pay_status,
                due_date=fee.due_date
            ))

        return StudentFeeSummary(
            student_id=student.id,
            student_name=student.user.full_name if student.user else "",
            admission_number=student.admission_number,
            class_name=student.class_obj.name if student.class_obj else None,
            total_fees=round(total_fees, 2),
            total_paid=round(total_paid, 2),
            remaining_balance=round(max(0.0, total_fees - total_paid), 2),
            items=items
        )

fee_service = FeeService()
