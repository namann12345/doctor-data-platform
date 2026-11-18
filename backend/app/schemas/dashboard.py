from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class DashboardStats(BaseModel):
    total_credits_purchased: int
    total_credits_spent: int
    current_balance: int
    total_doctors_unlocked: int
    total_payments: int
    successful_payments: int
    failed_payments: int
    total_spent_amount: float


class RecentActivity(BaseModel):
    id: int
    activity_type: str  # payment, unlock
    description: str
    credits_delta: int
    created_at: datetime


class DashboardResponse(BaseModel):
    stats: DashboardStats
    recent_activities: List[RecentActivity]
    unlocked_doctor_ids: List[int]


class AdminStats(BaseModel):
    total_users: int
    active_users: int
    total_doctors: int
    total_credits_sold: int
    total_revenue: float
    total_unlocks: int
    top_specialties: List[dict]
    top_cities: List[dict]
