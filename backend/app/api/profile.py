from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.user_repo import UserRepository
from app.schemas.auth import UserResponse, PasswordChange
from app.services.auth_service import AuthService
from app.dependencies import get_current_user

router = APIRouter(tags=["Profile"])


@router.get("", response_model=UserResponse)
def get_profile(current_user=Depends(get_current_user)):
    """Get current user profile."""
    return current_user


@router.put("", response_model=UserResponse)
def update_profile(
    data: dict,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update profile (full_name, phone)."""
    repo = UserRepository(db)
    allowed = {k: v for k, v in data.items() if k in ("full_name", "phone")}
    if not allowed:
        raise HTTPException(status_code=400, detail="No valid fields to update")
    user = repo.update_profile(current_user.id, **allowed)
    return user


@router.post("/change-password")
def change_password(
    data: PasswordChange,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Change password."""
    service = AuthService(db)
    service.change_password(current_user.id, data.current_password, data.new_password)
    return {"message": "Password changed successfully"}
