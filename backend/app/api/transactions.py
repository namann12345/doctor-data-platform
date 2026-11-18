from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.services.credit_service import CreditService
from app.repositories.transaction_repo import TransactionRepository
from app.dependencies import get_current_user

router = APIRouter(tags=["Transactions"])


@router.get("")
def list_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    transaction_type: Optional[str] = Query(None),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all transactions for current user (credit purchases + doctor unlocks)."""
    repo = TransactionRepository(db)
    txns, total = repo.list_for_user(current_user.id, skip=skip, limit=limit)
    page = skip // limit + 1 if limit > 0 else 1
    return {
        "transactions": [
            {
                "id": t.id,
                "transaction_type": t.transaction_type,
                "credits_delta": t.credits_delta,
                "balance_after": t.balance_after,
                "description": t.description,
                "created_at": t.created_at,
            }
            for t in txns
        ],
        "total": total,
        "page": page,
        "page_size": limit,
    }


@router.get("/payments")
def list_payments(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List payment history for current user."""
    service = CreditService(db)
    payments, total = service.get_payments(current_user.id, skip=skip, limit=limit)
    page = skip // limit + 1 if limit > 0 else 1
    return {
        "payments": [
            {
                "id": p.id,
                "credit_package_id": p.credit_package_id,
                "amount": p.amount,
                "credits_purchased": p.credits_purchased,
                "bonus_credits": p.bonus_credits,
                "status": p.status,
                "payment_mode": p.payment_mode,
                "gateway_reference": p.gateway_reference,
                "failure_reason": p.failure_reason,
                "created_at": p.created_at,
            }
            for p in payments
        ],
        "total": total,
        "page": page,
        "page_size": limit,
    }
