from sqlalchemy.orm import Session
from typing import Optional, List, Tuple
from fastapi import HTTPException
from app.repositories.doctor_repo import DoctorRepository
from app.models.doctor import Doctor


class DoctorService:
    def __init__(self, db: Session):
        self.db = db
        self.doctor_repo = DoctorRepository(db)

    def search_doctors(
        self,
        user_id: int,
        specialty: str = None,
        city: str = None,
        state: str = None,
        min_experience: int = None,
        max_fee: float = None,
        search: str = None,
        page: int = 1,
        page_size: int = 20,
    ) -> dict:
        skip = (page - 1) * page_size
        doctors, total = self.doctor_repo.search(
            specialty=specialty,
            city=city,
            state=state,
            min_experience=min_experience,
            max_fee=max_fee,
            search=search,
            skip=skip,
            limit=page_size,
        )

        unlocked_ids = set(self.doctor_repo.get_unlocked_doctor_ids(user_id))

        doctor_list = []
        for doc in doctors:
            d = {
                "id": doc.id,
                "name": doc.name,
                "specialty": doc.specialty,
                "qualification": doc.qualification,
                "experience_years": doc.experience_years,
                "hospital": doc.hospital,
                "city": doc.city,
                "state": doc.state,
                "consultation_fee": doc.consultation_fee,
                "rating": doc.rating,
                "total_reviews": doc.total_reviews,
                "bio": doc.bio,
                "is_unlocked": doc.id in unlocked_ids,
            }
            doctor_list.append(d)

        import math
        total_pages = math.ceil(total / page_size) if total > 0 else 1

        return {
            "doctors": doctor_list,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        }

    def get_doctor_detail(self, doctor_id: int, user_id: int) -> dict:
        doctor = self.doctor_repo.get_by_id(doctor_id)
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")

        unlock = self.doctor_repo.get_unlock(user_id, doctor_id)
        is_unlocked = unlock is not None

        result = {
            "id": doctor.id,
            "name": doctor.name,
            "specialty": doctor.specialty,
            "qualification": doctor.qualification,
            "experience_years": doctor.experience_years,
            "hospital": doctor.hospital,
            "city": doctor.city,
            "state": doctor.state,
            "consultation_fee": doctor.consultation_fee,
            "rating": doctor.rating,
            "total_reviews": doctor.total_reviews,
            "bio": doctor.bio,
            "is_unlocked": is_unlocked,
        }

        if is_unlocked:
            result["phone"] = doctor.phone
            result["email"] = doctor.email
            result["unlocked_at"] = unlock.unlocked_at
        else:
            result["phone"] = None
            result["email"] = None
            result["unlocked_at"] = None

        return result

    def create_doctor(self, **kwargs) -> Doctor:
        return self.doctor_repo.create(**kwargs)

    def update_doctor(self, doctor_id: int, **kwargs) -> Doctor:
        doctor = self.doctor_repo.update(doctor_id, **kwargs)
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")
        return doctor

    def delete_doctor(self, doctor_id: int) -> bool:
        success = self.doctor_repo.delete(doctor_id)
        if not success:
            raise HTTPException(status_code=404, detail="Doctor not found")
        return True
