from pydantic import BaseModel
from typing import List


class SpendingCoachResponse(BaseModel):
    financial_health_score: int
    health_status: str

    coach_tips: List[str]