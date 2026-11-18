from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class DoctorBase(BaseModel):
    name: str
    specialty: str
    qualification: Optional[str] = None
    experience_years: int = 0
    hospital: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    consultation_fee: Optional[float] = None
    rating: float = 0.0
    total_reviews: int = 0
    bio: Optional[str] = None


class DoctorCreate(DoctorBase):
    phone: Optional[str] = None
    email: Optional[EmailStr] = None


class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    specialty: Optional[str] = None
    qualification: Optional[str] = None
    experience_years: Optional[int] = None
    hospital: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    consultation_fee: Optional[float] = None
    rating: Optional[float] = None
    total_reviews: Optional[int] = None
    bio: Optional[str] = None
    is_active: Optional[bool] = None


class DoctorPublic(DoctorBase):
    """Public view - no contact info unless unlocked"""
    id: int
    is_unlocked: bool = False

    class Config:
        from_attributes = True


class DoctorDetail(DoctorBase):
    """Detailed view after unlock - includes contact info"""
    id: int
    phone: Optional[str] = None
    email: Optional[str] = None
    is_unlocked: bool = True
    unlocked_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DoctorListResponse(BaseModel):
    doctors: List[DoctorPublic]
    total: int
    page: int
    page_size: int
    total_pages: int


class DoctorFilters(BaseModel):
    specialty: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    min_experience: Optional[int] = None
    max_fee: Optional[float] = None
    search: Optional[str] = None
