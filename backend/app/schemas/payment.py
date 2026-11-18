from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class PaymentResponse(BaseModel):
    id: int
    user_id: int
    credit_package_id: int
    amount: float
    credits_purchased: int
    bonus_credits: int
    status: str
    payment_mode: str
    idempotency_key: Optional[str] = None
    gateway_reference: Optional[str] = None
    failure_reason: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class PaymentListResponse(BaseModel):
    payments: List[PaymentResponse]
    total: int
    page: int
    page_size: int
