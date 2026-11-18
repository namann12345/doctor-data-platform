from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.user import User
from app.utils.security import hash_password


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def create(self, email: str, password: str, full_name: str, phone: str = None, is_admin: bool = False) -> User:
        user = User(
            email=email,
            hashed_password=hash_password(password),
            full_name=full_name,
            phone=phone,
            is_admin=is_admin,
            credit_balance=0,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_balance(self, user_id: int, new_balance: int) -> Optional[User]:
        user = self.get_by_id(user_id)
        if user:
            user.credit_balance = new_balance
            self.db.commit()
            self.db.refresh(user)
        return user

    def update_profile(self, user_id: int, **kwargs) -> Optional[User]:
        user = self.get_by_id(user_id)
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key) and value is not None:
                    setattr(user, key, value)
            self.db.commit()
            self.db.refresh(user)
        return user

    def list_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.db.query(User).offset(skip).limit(limit).all()

    def count_all(self) -> int:
        return self.db.query(User).count()

    def count_active(self) -> int:
        return self.db.query(User).filter(User.is_active == True).count()
