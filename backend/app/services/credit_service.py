import uuid
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.repositories.credit_repo import CreditRepository
from app.repositories.transaction_repo import TransactionRepository
from app.repositories.user_repo import UserRepository
from app.repositories.doctor_repo import DoctorRepository
from app.config import settings


class CreditService:
    def __init__(self, db: Session):
        self.db = db
        self.credit_repo = CreditRepository(db)
        self.txn_repo = TransactionRepository(db)
        self.user_repo = UserRepository(db)
        self.doctor_repo = DoctorRepository(db)

    def list_packages(self):
        packages = self.credit_repo.list_packages()
        result = []
        for pkg in packages:
            result.append({
                "id": pkg.id,
                "name": pkg.name,
                "description": pkg.description,
                "credits": pkg.credits,
                "bonus_credits": pkg.bonus_credits,
                "total_credits": pkg.total_credits,
                "price": pkg.price,
                "price_per_credit": pkg.price_per_credit,
                "is_active": pkg.is_active,
                "is_featured": pkg.is_featured,
            })
        return result

    def purchase_credits(
        self,
        user_id: int,
        package_id: int,
        payment_mode: str = "success",
        idempotency_key: str = None,
    ) -> dict:
        """
        Atomic, idempotent credit purchase.
        payment_mode: 'success' | 'fail' | 'pending'
        """
        # 1. Idempotency check - return existing if found
        if idempotency_key:
            existing_payment = self.credit_repo.get_payment_by_idempotency_key(idempotency_key)
            if existing_payment:
                user = self.user_repo.get_by_id(user_id)
                return {
                    "payment_id": existing_payment.id,
                    "status": existing_payment.status,
                    "credits_added": existing_payment.credits_purchased if existing_payment.status == "success" else 0,
                    "bonus_credits": existing_payment.bonus_credits if existing_payment.status == "success" else 0,
                    "new_balance": user.credit_balance,
                    "message": "Duplicate request - returning existing payment",
                }

        # 2. Validate package
        package = self.credit_repo.get_package(package_id)
        if not package:
            raise HTTPException(status_code=404, detail="Credit package not found or inactive")

        # 3. Get user
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        try:
            # 4. Create pending payment
            payment = self.credit_repo.create_payment(
                user_id=user_id,
                credit_package_id=package_id,
                amount=package.price,
                credits_purchased=package.credits,
                bonus_credits=package.bonus_credits,
                status="pending",
                payment_mode=payment_mode,
                idempotency_key=idempotency_key or str(uuid.uuid4()),
                gateway_reference=f"GW-{uuid.uuid4().hex[:12].upper()}",
            )
            self.db.flush()

            # 5. Simulate payment gateway response
            if payment_mode == "fail":
                # Payment failed - update status, no credits added
                self.credit_repo.update_payment(
                    payment,
                    status="failed",
                    failure_reason="Payment declined by gateway (simulated failure)",
                )
                self.db.commit()
                return {
                    "payment_id": payment.id,
                    "status": "failed",
                    "credits_added": 0,
                    "bonus_credits": 0,
                    "new_balance": user.credit_balance,
                    "message": "Payment failed - no credits added",
                }

            elif payment_mode == "pending":
                # Payment pending - awaiting webhook (reconciliation scenario)
                self.db.commit()
                return {
                    "payment_id": payment.id,
                    "status": "pending",
                    "credits_added": 0,
                    "bonus_credits": 0,
                    "new_balance": user.credit_balance,
                    "message": "Payment pending - credits will be added upon confirmation",
                }

            else:  # success
                # 6. Atomic: update payment + add credits + ledger + transaction
                total_credits = package.total_credits
                old_balance = user.credit_balance
                new_balance = old_balance + total_credits

                # Update payment status
                self.credit_repo.update_payment(payment, status="success")

                # Update user balance (within same transaction)
                user.credit_balance = new_balance
                self.db.flush()

                # Create ledger entry
                self.credit_repo.create_ledger_entry(
                    user_id=user_id,
                    payment_id=payment.id,
                    entry_type="credit",
                    credits=total_credits,
                    balance_before=old_balance,
                    balance_after=new_balance,
                    reference=payment.gateway_reference,
                    notes=f"Purchased {package.name}: {package.credits} + {package.bonus_credits} bonus credits",
                )

                # Create transaction record
                self.txn_repo.create(
                    user_id=user_id,
                    payment_id=payment.id,
                    transaction_type="credit_purchase",
                    credits_delta=total_credits,
                    balance_after=new_balance,
                    description=f"Purchased package: {package.name}",
                )

                # Commit entire atomic block
                self.db.commit()

                return {
                    "payment_id": payment.id,
                    "status": "success",
                    "credits_added": package.credits,
                    "bonus_credits": package.bonus_credits,
                    "new_balance": new_balance,
                    "message": f"Successfully purchased {total_credits} credits",
                }

        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Duplicate payment detected. Use a unique idempotency key.",
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Payment processing error: {str(e)}")

    def unlock_doctor(self, user_id: int, doctor_id: int) -> dict:
        """
        Atomic doctor unlock.
        - Returns existing unlock if already done (no charge).
        - Raises 402 if insufficient credits.
        - Atomically deducts credits + creates ledger + unlock record.
        """
        cost = settings.CREDIT_COST_PER_PROFILE

        # 1. Check if already unlocked (idempotent - no double charge)
        existing_unlock = self.credit_repo.get_unlock(user_id, doctor_id)
        if existing_unlock:
            user = self.user_repo.get_by_id(user_id)
            return {
                "doctor_id": doctor_id,
                "already_unlocked": True,
                "credits_spent": 0,
                "new_balance": user.credit_balance,
                "message": "Doctor already unlocked - no additional charge",
            }

        # 2. Validate doctor exists
        doctor = self.doctor_repo.get_by_id(doctor_id)
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")

        # 3. Get user and verify balance
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.credit_balance < cost:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail=f"Insufficient credits. Required: {cost}, Available: {user.credit_balance}",
            )

        try:
            # 4. Atomic unlock: deduct credits + create unlock record + ledger + transaction
            old_balance = user.credit_balance
            new_balance = old_balance - cost

            # Update user balance
            user.credit_balance = new_balance
            self.db.flush()

            # Create unlock record
            unlock = self.credit_repo.create_unlock(
                user_id=user_id,
                doctor_id=doctor_id,
                credits_spent=cost,
            )

            # Create ledger entry
            self.credit_repo.create_ledger_entry(
                user_id=user_id,
                doctor_unlock_id=unlock.id,
                entry_type="debit",
                credits=cost,
                balance_before=old_balance,
                balance_after=new_balance,
                reference=f"UNLOCK-{doctor_id}",
                notes=f"Unlocked Dr. {doctor.name} ({doctor.specialty})",
            )

            # Create transaction record
            self.txn_repo.create(
                user_id=user_id,
                doctor_unlock_id=unlock.id,
                transaction_type="doctor_unlock",
                credits_delta=-cost,
                balance_after=new_balance,
                description=f"Unlocked Dr. {doctor.name} - {doctor.specialty}",
            )

            # Commit all atomically
            self.db.commit()

            return {
                "doctor_id": doctor_id,
                "already_unlocked": False,
                "credits_spent": cost,
                "new_balance": new_balance,
                "message": f"Dr. {doctor.name} unlocked successfully",
            }

        except IntegrityError:
            self.db.rollback()
            # Race condition - doctor was already unlocked concurrently
            user = self.user_repo.get_by_id(user_id)
            return {
                "doctor_id": doctor_id,
                "already_unlocked": True,
                "credits_spent": 0,
                "new_balance": user.credit_balance,
                "message": "Doctor already unlocked (concurrent request)",
            }
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Unlock error: {str(e)}")

    def reconcile_payment(self, payment_id: int, admin_user_id: int) -> dict:
        """
        Reconciliation: Handle the scenario where payment was successful
        but credits were never added (pending status).
        """
        payment = self.credit_repo.get_payment(payment_id)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")

        if payment.status == "success":
            return {"message": "Payment already successfully processed", "payment_id": payment_id}

        if payment.status == "failed":
            raise HTTPException(status_code=400, detail="Cannot reconcile a failed payment")

        # It's pending - force complete it
        try:
            user = self.user_repo.get_by_id(payment.user_id)
            package = self.credit_repo.get_package(payment.credit_package_id)
            total_credits = payment.credits_purchased + payment.bonus_credits
            old_balance = user.credit_balance
            new_balance = old_balance + total_credits

            self.credit_repo.update_payment(payment, status="success")
            user.credit_balance = new_balance
            self.db.flush()

            self.credit_repo.create_ledger_entry(
                user_id=payment.user_id,
                payment_id=payment.id,
                entry_type="credit",
                credits=total_credits,
                balance_before=old_balance,
                balance_after=new_balance,
                reference=payment.gateway_reference,
                notes=f"Reconciled payment #{payment_id}",
            )

            self.txn_repo.create(
                user_id=payment.user_id,
                payment_id=payment.id,
                transaction_type="credit_purchase",
                credits_delta=total_credits,
                balance_after=new_balance,
                description=f"Reconciled payment #{payment_id}",
            )

            self.db.commit()
            return {
                "message": "Payment reconciled successfully",
                "payment_id": payment_id,
                "credits_added": total_credits,
                "new_balance": new_balance,
            }
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Reconciliation error: {str(e)}")

    def get_credit_ledger(self, user_id: int, skip: int = 0, limit: int = 50):
        return self.credit_repo.list_ledger(user_id, skip=skip, limit=limit)

    def get_payments(self, user_id: int, skip: int = 0, limit: int = 20):
        return self.credit_repo.list_payments(user_id, skip=skip, limit=limit)
