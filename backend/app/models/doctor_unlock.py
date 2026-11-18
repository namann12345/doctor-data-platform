from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class DoctorUnlock(Base):
    __tablename__ = "doctor_unlocks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False, index=True)
    credits_spent = Column(Integer, nullable=False)
    unlocked_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "doctor_id", name="uq_user_doctor_unlock"),
    )

    # Relationships
    user = relationship("User", back_populates="doctor_unlocks")
    doctor = relationship("Doctor", back_populates="unlocks")
    transactions = relationship("Transaction", back_populates="doctor_unlock")
    ledger_entries = relationship("CreditLedger", back_populates="doctor_unlock")
