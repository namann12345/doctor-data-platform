from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CreditPackageResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    credits: int
    bonus_credits: int
    total_credits: int
    price: float
    price_per_credit: float
    is_active: bool
    is_featured: bool

    class Config:
        from_attributes = True


class PurchaseCreditsRequest(BaseModel):
    package_id: int
    payment_mode: str = Field(default="success", pattern="^(success|fail|pending)$")
    idempotency_key: Optional[str] = None


class PurchaseCreditsResponse(BaseModel):
    payment_id: int
    status: str
    credits_added: int
    bonus_credits: int
    new_balance: int
    message: str


class UnlockDoctorRequest(BaseModel):
    doctor_id: int


class UnlockDoctorResponse(BaseModel):
    doctor_id: int
    already_unlocked: bool
    credits_spent: int
    new_balance: int
    message: str


class CreditBalanceResponse(BaseModel):
    user_id: int
    credit_balance: int


class CreditLedgerEntry(BaseModel):
    id: int
    entry_type: str
    credits: int
    balance_before: int
    balance_after: int
    reference: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
