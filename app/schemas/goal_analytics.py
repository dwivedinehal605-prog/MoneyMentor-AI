
from pydantic import BaseModel


class GoalProgress(BaseModel):
    title: str
    target_amount: float
    saved_amount: float
    remaining_amount: float
    progress_percentage: float
    days_left: int
    monthly_required_saving: float
    priority: str
    status: str
    is_on_track: bool


class GoalAnalyticsResponse(BaseModel):
    total_goals: int
    completed_goals: int
    active_goals: int

    total_target_amount: float
    total_saved_amount: float
    total_remaining_amount: float

    overall_progress_percentage: float
    goal_completion_rate: float

    high_priority_goals: int
    medium_priority_goals: int
    low_priority_goals: int

    monthly_saving_needed_all_goals: float

    goals: list[GoalProgress]