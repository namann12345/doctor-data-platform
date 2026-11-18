from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.services.credit_service import CreditService
from app.schemas.credit import (
    CreditPackageResponse,
    PurchaseCreditsRequest,
    PurchaseCreditsResponse,
    UnlockDoctorRequest,
    UnlockDoctorResponse,
    CreditBalanceResponse,
    CreditLedgerEntry,
)
from app.dependencies import get_current_user, get_current_admin

router = APIRouter(tags=["Credits"])


@router.get("/packages")
def list_packages(db: Session = Depends(get_db)):
    """List all available credit packages."""
    service = CreditService(db)
    return service.list_packages()


@router.post("/purchase", response_model=PurchaseCreditsResponse)
def purchase_credits(
    data: PurchaseCreditsRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Purchase credits. payment_mode: 'success' | 'fail' | 'pending'
    - success: Credits added immediately
    - fail: Payment declined, no credits
    - pending: Awaiting confirmation (reconciliation needed)
    Idempotency key prevents duplicate purchases.
    """
    service = CreditService(db)
    return service.purchase_credits(
        user_id=current_user.id,
        package_id=data.package_id,
        payment_mode=data.payment_mode,
        idempotency_key=data.idempotency_key,
    )


@router.post("/unlock", response_model=UnlockDoctorResponse)
def unlock_doctor(
    data: UnlockDoctorRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Unlock a doctor profile to reveal contact info.
    - 10 credits per unlock
    - Already unlocked doctors: no charge
    - Insufficient credits: 402 error
    """
    service = CreditService(db)
    return service.unlock_doctor(user_id=current_user.id, doctor_id=data.doctor_id)


@router.get("/balance", response_model=CreditBalanceResponse)
def get_balance(current_user=Depends(get_current_user)):
    """Get current credit balance."""
    return {"user_id": current_user.id, "credit_balance": current_user.credit_balance}


@router.get("/ledger")
def get_ledger(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get credit ledger history."""
    service = CreditService(db)
    entries = service.get_credit_ledger(current_user.id, skip=skip, limit=limit)
    return [
        {
            "id": e.id,
            "entry_type": e.entry_type,
            "credits": e.credits,
            "balance_before": e.balance_before,
            "balance_after": e.balance_after,
            "reference": e.reference,
            "notes": e.notes,
            "created_at": e.created_at,
        }
        for e in entries
    ]


@router.post("/reconcile/{payment_id}")
def reconcile_payment(
    payment_id: int,
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """
    Admin: Reconcile a pending payment - force-complete it and add credits.
    Handles the scenario: payment success but credits not added.
    """
    service = CreditService(db)
    return service.reconcile_payment(payment_id, current_admin.id)
