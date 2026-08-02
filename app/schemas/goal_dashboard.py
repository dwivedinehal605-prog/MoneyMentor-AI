from pydantic import BaseModel


class GoalDashboardResponse(BaseModel):
    title: str
    target_amount: float
    saved_amount: float
    remaining_amount: float
    progress_percentage: float
    status: str

    days_remaining: int

    recommended_daily_saving: float

    recommended_monthly_saving: float