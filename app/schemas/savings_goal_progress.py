from pydantic import BaseModel


class SavingsGoalProgressItem(BaseModel):
    title: str
    target_amount: float
    saved_amount: float
    remaining_amount: float
    progress_percentage: float
    status: str


class SavingsGoalProgressResponse(BaseModel):
    goals: list[SavingsGoalProgressItem]