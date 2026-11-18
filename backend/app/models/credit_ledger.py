from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class CreditLedger(Base):
    __tablename__ = "credit_ledger"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    payment_id = Column(Integer, ForeignKey("payments.id"), nullable=True)
    doctor_unlock_id = Column(Integer, ForeignKey("doctor_unlocks.id"), nullable=True)
    entry_type = Column(String, nullable=False)  # credit, debit
    credits = Column(Integer, nullable=False)  # always positive
    balance_before = Column(Integer, nullable=False)
    balance_after = Column(Integer, nullable=False)
    reference = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="credit_ledger")
    payment = relationship("Payment", back_populates="ledger_entries")
    doctor_unlock = relationship("DoctorUnlock", back_populates="ledger_entries")
