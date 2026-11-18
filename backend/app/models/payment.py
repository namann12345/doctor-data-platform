from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    credit_package_id = Column(Integer, ForeignKey("credit_packages.id"), nullable=False)
    amount = Column(Float, nullable=False)
    credits_purchased = Column(Integer, nullable=False)
    bonus_credits = Column(Integer, default=0)
    status = Column(String, default="pending")  # pending, success, failed
    payment_mode = Column(String, default="success")  # success, fail, pending (simulation)
    idempotency_key = Column(String, unique=True, index=True, nullable=True)
    gateway_reference = Column(String, nullable=True)
    failure_reason = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="payments")
    credit_package = relationship("CreditPackage", back_populates="payments")
    transactions = relationship("Transaction", back_populates="payment")
    ledger_entries = relationship("CreditLedger", back_populates="payment")
