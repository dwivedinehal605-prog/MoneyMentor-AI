from pydantic import BaseModel


class GoalProgressResponse(BaseModel):
    title: str
    target_amount: float
    saved_amount: float
    remaining_amount: float
    progress_percentage: float
    status: str