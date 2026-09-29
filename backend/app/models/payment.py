from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    fee_id = Column(Integer, ForeignKey("fees.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    amount_paid = Column(Float, nullable=False)
    payment_date = Column(Date, nullable=False)
    payment_method = Column(String(50), default="Cash")  # Cash, Bank Transfer, Online, Cheque
    payment_status = Column(String(20), default="PAID", nullable=False)  # PAID, PARTIAL, PENDING
    transaction_id = Column(String(100), unique=True, nullable=True)
    remarks = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    fee = relationship("Fee", back_populates="payments")
    student = relationship("Student", back_populates="payments")
