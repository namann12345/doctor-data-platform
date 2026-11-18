from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.dashboard_service import DashboardService
from app.services.doctor_service import DoctorService
from app.schemas.doctor import DoctorCreate, DoctorUpdate
from app.repositories.user_repo import UserRepository
from app.dependencies import get_current_admin

router = APIRouter(tags=["Admin"])


@router.get("/stats")
def get_admin_stats(
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Admin: Platform-wide statistics."""
    service = DashboardService(db)
    return service.get_admin_stats()


@router.get("/users")
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Admin: List all users."""
    repo = UserRepository(db)
    users = repo.list_all(skip=skip, limit=limit)
    total = repo.count_all()
    return {
        "users": [
            {
                "id": u.id,
                "email": u.email,
                "full_name": u.full_name,
                "phone": u.phone,
                "credit_balance": u.credit_balance,
                "is_active": u.is_active,
                "is_admin": u.is_admin,
                "created_at": u.created_at,
            }
            for u in users
        ],
        "total": total,
    }


@router.post("/doctors", status_code=201)
def create_doctor(
    data: DoctorCreate,
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Admin: Create a new doctor."""
    service = DoctorService(db)
    doctor = service.create_doctor(**data.model_dump())
    return {"id": doctor.id, "name": doctor.name, "specialty": doctor.specialty}


@router.put("/doctors/{doctor_id}")
def update_doctor(
    doctor_id: int,
    data: DoctorUpdate,
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Admin: Update a doctor."""
    service = DoctorService(db)
    doctor = service.update_doctor(doctor_id, **data.model_dump(exclude_none=True))
    return {"id": doctor.id, "name": doctor.name, "specialty": doctor.specialty}


@router.delete("/doctors/{doctor_id}")
def delete_doctor(
    doctor_id: int,
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Admin: Soft-delete a doctor."""
    service = DoctorService(db)
    service.delete_doctor(doctor_id)
    return {"message": "Doctor deactivated successfully"}
