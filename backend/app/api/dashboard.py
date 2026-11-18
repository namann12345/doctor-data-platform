from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.dashboard_service import DashboardService
from app.schemas.dashboard import DashboardResponse
from app.dependencies import get_current_user

router = APIRouter(tags=["Dashboard"])


@router.get("", response_model=DashboardResponse)
def get_dashboard(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get user dashboard: stats, recent activity, unlocked doctors."""
    service = DashboardService(db)
    return service.get_user_dashboard(current_user.id)
