from pydantic import BaseModel
from typing import List


class RecommendationResponse(BaseModel):
    financial_health: str
    recommendations: List[str]