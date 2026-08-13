from pydantic import BaseModel
from datetime import date


class GoalProgressResponse(BaseModel):
    title: str
    target_amount: float
    saved_amount: float
    remaining_amount: float
    progress_percentage: float

    deadline: date
    days_remaining: int
    required_monthly_saving: float

    status: str
    recommendation: str