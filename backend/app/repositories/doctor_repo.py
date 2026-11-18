from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import Optional, List, Tuple
from app.models.doctor import Doctor
from app.models.doctor_unlock import DoctorUnlock


class DoctorRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, doctor_id: int) -> Optional[Doctor]:
        return self.db.query(Doctor).filter(Doctor.id == doctor_id, Doctor.is_active == True).first()

    def get_by_id_any(self, doctor_id: int) -> Optional[Doctor]:
        return self.db.query(Doctor).filter(Doctor.id == doctor_id).first()

    def search(
        self,
        specialty: str = None,
        city: str = None,
        state: str = None,
        min_experience: int = None,
        max_fee: float = None,
        search: str = None,
        skip: int = 0,
        limit: int = 20,
    ) -> Tuple[List[Doctor], int]:
        query = self.db.query(Doctor).filter(Doctor.is_active == True)

        if specialty:
            query = query.filter(Doctor.specialty.ilike(f"%{specialty}%"))
        if city:
            query = query.filter(Doctor.city.ilike(f"%{city}%"))
        if state:
            query = query.filter(Doctor.state.ilike(f"%{state}%"))
        if min_experience is not None:
            query = query.filter(Doctor.experience_years >= min_experience)
        if max_fee is not None:
            query = query.filter(Doctor.consultation_fee <= max_fee)
        if search:
            query = query.filter(
                or_(
                    Doctor.name.ilike(f"%{search}%"),
                    Doctor.specialty.ilike(f"%{search}%"),
                    Doctor.hospital.ilike(f"%{search}%"),
                    Doctor.city.ilike(f"%{search}%"),
                )
            )

        total = query.count()
        doctors = query.offset(skip).limit(limit).all()
        return doctors, total

    def create(self, **kwargs) -> Doctor:
        doctor = Doctor(**kwargs)
        self.db.add(doctor)
        self.db.commit()
        self.db.refresh(doctor)
        return doctor

    def update(self, doctor_id: int, **kwargs) -> Optional[Doctor]:
        doctor = self.get_by_id_any(doctor_id)
        if doctor:
            for key, value in kwargs.items():
                if hasattr(doctor, key) and value is not None:
                    setattr(doctor, key, value)
            self.db.commit()
            self.db.refresh(doctor)
        return doctor

    def delete(self, doctor_id: int) -> bool:
        doctor = self.get_by_id_any(doctor_id)
        if doctor:
            doctor.is_active = False
            self.db.commit()
            return True
        return False

    def count_all(self) -> int:
        return self.db.query(Doctor).filter(Doctor.is_active == True).count()

    def get_unlock(self, user_id: int, doctor_id: int) -> Optional[DoctorUnlock]:
        return (
            self.db.query(DoctorUnlock)
            .filter(DoctorUnlock.user_id == user_id, DoctorUnlock.doctor_id == doctor_id)
            .first()
        )

    def get_unlocked_doctor_ids(self, user_id: int) -> List[int]:
        rows = self.db.query(DoctorUnlock.doctor_id).filter(DoctorUnlock.user_id == user_id).all()
        return [r[0] for r in rows]

    def get_specialties(self) -> List[dict]:
        from sqlalchemy import func
        rows = (
            self.db.query(Doctor.specialty, func.count(Doctor.id).label("count"))
            .filter(Doctor.is_active == True)
            .group_by(Doctor.specialty)
            .order_by(func.count(Doctor.id).desc())
            .limit(10)
            .all()
        )
        return [{"specialty": r[0], "count": r[1]} for r in rows]

    def get_cities(self) -> List[dict]:
        from sqlalchemy import func
        rows = (
            self.db.query(Doctor.city, func.count(Doctor.id).label("count"))
            .filter(Doctor.is_active == True, Doctor.city.isnot(None))
            .group_by(Doctor.city)
            .order_by(func.count(Doctor.id).desc())
            .limit(10)
            .all()
        )
        return [{"city": r[0], "count": r[1]} for r in rows]
