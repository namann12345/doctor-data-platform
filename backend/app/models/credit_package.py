from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class CreditPackage(Base):
    __tablename__ = "credit_packages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    credits = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    bonus_credits = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    payments = relationship("Payment", back_populates="credit_package")

    @property
    def total_credits(self):
        return self.credits + self.bonus_credits

    @property
    def price_per_credit(self):
        if self.total_credits == 0:
            return 0
        return round(self.price / self.total_credits, 4)
