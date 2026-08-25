from pydantic import BaseModel


class GoalRecommendationResponse(BaseModel):
    title: str

    target_amount: float
    saved_amount: float

    remaining_amount: float

    months_left: int

    required_monthly_saving: float
    required_daily_saving: float

    goal_probability: str

    recommendation: str