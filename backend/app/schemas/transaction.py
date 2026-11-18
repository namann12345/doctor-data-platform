from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class TransactionResponse(BaseModel):
    id: int
    user_id: int
    transaction_type: str
    credits_delta: int
    balance_after: int
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class TransactionListResponse(BaseModel):
    transactions: List[TransactionResponse]
    total: int
    page: int
    page_size: int
