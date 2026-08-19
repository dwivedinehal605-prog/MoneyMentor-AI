from pydantic import BaseModel


class OverallSpendingRiskResponse(BaseModel):
    total_expense: float
    top_category: str
    top_category_percentage: float
    risk_score: int
    risk_status: str
    message: str
