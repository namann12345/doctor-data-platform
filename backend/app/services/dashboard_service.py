from sqlalchemy.orm import Session
from app.repositories.credit_repo import CreditRepository
from app.repositories.transaction_repo import TransactionRepository
from app.repositories.user_repo import UserRepository
from app.repositories.doctor_repo import DoctorRepository


class DashboardService:
    def __init__(self, db: Session):
        self.db = db
        self.credit_repo = CreditRepository(db)
        self.txn_repo = TransactionRepository(db)
        self.user_repo = UserRepository(db)
        self.doctor_repo = DoctorRepository(db)

    def get_user_dashboard(self, user_id: int) -> dict:
        user = self.user_repo.get_by_id(user_id)
        total_purchased = self.credit_repo.total_credits_purchased(user_id)
        total_spent = self.credit_repo.total_credits_spent(user_id)
        total_unlocks = self.credit_repo.count_unlocks(user_id)
        total_payments = self.credit_repo.total_payments_count(user_id)
        successful_payments = self.credit_repo.total_successful_payments(user_id)
        failed_payments = self.credit_repo.total_failed_payments(user_id)
        total_amount = self.credit_repo.total_amount_spent(user_id)

        unlocked_ids = self.doctor_repo.get_unlocked_doctor_ids(user_id)

        # Recent transactions as activities
        txns, _ = self.txn_repo.list_for_user(user_id, skip=0, limit=10)
        activities = []
        for txn in txns:
            activities.append({
                "id": txn.id,
                "activity_type": "unlock" if txn.transaction_type == "doctor_unlock" else "payment",
                "description": txn.description or txn.transaction_type,
                "credits_delta": txn.credits_delta,
                "created_at": txn.created_at,
            })

        return {
            "stats": {
                "total_credits_purchased": total_purchased,
                "total_credits_spent": total_spent,
                "current_balance": user.credit_balance,
                "total_doctors_unlocked": total_unlocks,
                "total_payments": total_payments,
                "successful_payments": successful_payments,
                "failed_payments": failed_payments,
                "total_spent_amount": total_amount,
            },
            "recent_activities": activities,
            "unlocked_doctor_ids": unlocked_ids,
        }

    def get_admin_stats(self) -> dict:
        from sqlalchemy import func
        from app.models.payment import Payment
        from app.models.doctor_unlock import DoctorUnlock

        total_users = self.user_repo.count_all()
        active_users = self.user_repo.count_active()
        total_doctors = self.doctor_repo.count_all()

        total_credits_sold = (
            self.db.query(func.sum(Payment.credits_purchased + Payment.bonus_credits))
            .filter(Payment.status == "success")
            .scalar() or 0
        )
        total_revenue = (
            self.db.query(func.sum(Payment.amount))
            .filter(Payment.status == "success")
            .scalar() or 0.0
        )
        total_unlocks = self.db.query(DoctorUnlock).count()

        top_specialties = self.doctor_repo.get_specialties()
        top_cities = self.doctor_repo.get_cities()

        return {
            "total_users": total_users,
            "active_users": active_users,
            "total_doctors": total_doctors,
            "total_credits_sold": int(total_credits_sold),
            "total_revenue": float(total_revenue),
            "total_unlocks": total_unlocks,
            "top_specialties": top_specialties,
            "top_cities": top_cities,
        }
