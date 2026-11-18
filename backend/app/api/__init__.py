from app.api.auth import router as auth_router
from app.api.doctors import router as doctors_router
from app.api.credits import router as credits_router
from app.api.transactions import router as transactions_router
from app.api.dashboard import router as dashboard_router
from app.api.profile import router as profile_router
from app.api.admin import router as admin_router

__all__ = [
    "auth_router",
    "doctors_router",
    "credits_router",
    "transactions_router",
    "dashboard_router",
    "profile_router",
    "admin_router",
]
