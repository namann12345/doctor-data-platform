from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.services.doctor_service import DoctorService
from app.schemas.doctor import DoctorListResponse, DoctorDetail
from app.dependencies import get_current_user

router = APIRouter(tags=["Doctors"])


@router.get("", response_model=DoctorListResponse)
def search_doctors(
    specialty: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    min_experience: Optional[int] = Query(None, ge=0),
    max_fee: Optional[float] = Query(None, ge=0),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Search/filter doctors. Returns public info. Contact info hidden until unlocked."""
    service = DoctorService(db)
    return service.search_doctors(
        user_id=current_user.id,
        specialty=specialty,
        city=city,
        state=state,
        min_experience=min_experience,
        max_fee=max_fee,
        search=search,
        page=page,
        page_size=page_size,
    )


@router.get("/{doctor_id}")
def get_doctor(
    doctor_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get doctor details. Contact info only shown if unlocked."""
    service = DoctorService(db)
    return service.get_doctor_detail(doctor_id, current_user.id)
