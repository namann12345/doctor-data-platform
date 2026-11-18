from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.credit_package import CreditPackage
from app.models.payment import Payment
from app.models.credit_ledger import CreditLedger
from app.models.doctor_unlock import DoctorUnlock


class CreditRepository:
    def __init__(self, db: Session):
        self.db = db

    # --- Packages ---
    def get_package(self, package_id: int) -> Optional[CreditPackage]:
        return self.db.query(CreditPackage).filter(
            CreditPackage.id == package_id,
            CreditPackage.is_active == True
        ).first()

    def list_packages(self) -> List[CreditPackage]:
        return self.db.query(CreditPackage).filter(CreditPackage.is_active == True).all()

    def create_package(self, **kwargs) -> CreditPackage:
        pkg = CreditPackage(**kwargs)
        self.db.add(pkg)
        self.db.commit()
        self.db.refresh(pkg)
        return pkg

    # --- Payments ---
    def get_payment_by_idempotency_key(self, key: str) -> Optional[Payment]:
        return self.db.query(Payment).filter(Payment.idempotency_key == key).first()

    def get_payment(self, payment_id: int) -> Optional[Payment]:
        return self.db.query(Payment).filter(Payment.id == payment_id).first()

    def create_payment(self, **kwargs) -> Payment:
        payment = Payment(**kwargs)
        self.db.add(payment)
        self.db.flush()  # get ID without committing
        return payment

    def update_payment(self, payment: Payment, **kwargs) -> Payment:
        for key, value in kwargs.items():
            setattr(payment, key, value)
        self.db.flush()
        return payment

    def list_payments(self, user_id: int, skip: int = 0, limit: int = 20):
        query = self.db.query(Payment).filter(Payment.user_id == user_id).order_by(Payment.created_at.desc())
        total = query.count()
        payments = query.offset(skip).limit(limit).all()
        return payments, total

    # --- Ledger ---
    def create_ledger_entry(self, **kwargs) -> CreditLedger:
        entry = CreditLedger(**kwargs)
        self.db.add(entry)
        self.db.flush()
        return entry

    def list_ledger(self, user_id: int, skip: int = 0, limit: int = 50) -> List[CreditLedger]:
        return (
            self.db.query(CreditLedger)
            .filter(CreditLedger.user_id == user_id)
            .order_by(CreditLedger.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    # --- Unlocks ---
    def get_unlock(self, user_id: int, doctor_id: int) -> Optional[DoctorUnlock]:
        return self.db.query(DoctorUnlock).filter(
            DoctorUnlock.user_id == user_id,
            DoctorUnlock.doctor_id == doctor_id,
        ).first()

    def create_unlock(self, **kwargs) -> DoctorUnlock:
        unlock = DoctorUnlock(**kwargs)
        self.db.add(unlock)
        self.db.flush()
        return unlock

    def count_unlocks(self, user_id: int) -> int:
        return self.db.query(DoctorUnlock).filter(DoctorUnlock.user_id == user_id).count()

    def total_credits_purchased(self, user_id: int) -> int:
        from sqlalchemy import func
        result = self.db.query(func.sum(CreditLedger.credits)).filter(
            CreditLedger.user_id == user_id,
            CreditLedger.entry_type == "credit",
        ).scalar()
        return result or 0

    def total_credits_spent(self, user_id: int) -> int:
        from sqlalchemy import func
        result = self.db.query(func.sum(CreditLedger.credits)).filter(
            CreditLedger.user_id == user_id,
            CreditLedger.entry_type == "debit",
        ).scalar()
        return result or 0

    def total_payments_count(self, user_id: int) -> int:
        return self.db.query(Payment).filter(Payment.user_id == user_id).count()

    def total_successful_payments(self, user_id: int) -> int:
        return self.db.query(Payment).filter(
            Payment.user_id == user_id,
            Payment.status == "success",
        ).count()

    def total_failed_payments(self, user_id: int) -> int:
        return self.db.query(Payment).filter(
            Payment.user_id == user_id,
            Payment.status == "failed",
        ).count()

    def total_amount_spent(self, user_id: int) -> float:
        from sqlalchemy import func
        result = self.db.query(func.sum(Payment.amount)).filter(
            Payment.user_id == user_id,
            Payment.status == "success",
        ).scalar()
        return float(result or 0)
