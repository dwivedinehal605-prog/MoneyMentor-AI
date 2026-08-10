from pydantic import BaseModel
from datetime import date, datetime


class SavingsGoalCreate(BaseModel):
    title: str
    target_amount: float
    deadline: date


class SavingsGoalUpdate(BaseModel):
    title: str | None = None
    target_amount: float | None = None
    saved_amount: float | None = None
    deadline: date | None = None


class SavingsGoalResponse(BaseModel):
    id: int
    user_id: int
    title: str
    target_amount: float
    saved_amount: float
    deadline: date
    created_at: datetime

    class Config:
        from_attributes = True