from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth_service import AuthService
from app.schemas.auth import UserRegister, Token, UserResponse, PasswordChange
from app.dependencies import get_current_user

router = APIRouter(tags=["Authentication"])


@router.post("/register", response_model=Token, status_code=201)
def register(data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user account."""
    service = AuthService(db)
    return service.register(data)


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login with email and password. Returns JWT token."""
    service = AuthService(db)
    return service.login(email=form_data.username, password=form_data.password)


@router.post("/login/json", response_model=Token)
def login_json(data: dict, db: Session = Depends(get_db)):
    """Login with JSON body (email + password)."""
    service = AuthService(db)
    return service.login(email=data.get("email", ""), password=data.get("password", ""))


@router.get("/me", response_model=UserResponse)
def get_me(current_user=Depends(get_current_user)):
    """Get current user profile."""
    return current_user


@router.post("/change-password")
def change_password(
    data: PasswordChange,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Change current user password."""
    service = AuthService(db)
    service.change_password(current_user.id, data.current_password, data.new_password)
    return {"message": "Password changed successfully"}
