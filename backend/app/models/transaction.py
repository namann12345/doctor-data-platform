from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    payment_id = Column(Integer, ForeignKey("payments.id"), nullable=True)
    doctor_unlock_id = Column(Integer, ForeignKey("doctor_unlocks.id"), nullable=True)
    transaction_type = Column(String, nullable=False)  # credit_purchase, doctor_unlock, refund, bonus
    credits_delta = Column(Integer, nullable=False)  # positive=credit, negative=debit
    balance_after = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="transactions")
    payment = relationship("Payment", back_populates="transactions")
    doctor_unlock = relationship("DoctorUnlock", back_populates="transactions")
