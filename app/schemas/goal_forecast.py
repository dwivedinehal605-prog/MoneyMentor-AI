from typing import List

from pydantic import BaseModel


class GoalForecast(BaseModel):
    goal: str
    remaining_amount: float
    monthly_allocation: float
    months_to_complete: int


class GoalForecastResponse(BaseModel):
    forecasts: List[GoalForecast]