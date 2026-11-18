from sqlalchemy.orm import Session
from typing import List, Tuple
from app.models.transaction import Transaction


class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, **kwargs) -> Transaction:
        txn = Transaction(**kwargs)
        self.db.add(txn)
        self.db.flush()
        return txn

    def list_for_user(self, user_id: int, skip: int = 0, limit: int = 20) -> Tuple[List[Transaction], int]:
        query = (
            self.db.query(Transaction)
            .filter(Transaction.user_id == user_id)
            .order_by(Transaction.created_at.desc())
        )
        total = query.count()
        txns = query.offset(skip).limit(limit).all()
        return txns, total

    def list_all(self, skip: int = 0, limit: int = 50) -> List[Transaction]:
        return (
            self.db.query(Transaction)
            .order_by(Transaction.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
