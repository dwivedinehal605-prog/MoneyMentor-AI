from pydantic import BaseModel


class CategoryTrendScoreResponse(BaseModel):
    category: str
    current_month_expense: float
    previous_month_expense: float
    change_percentage: float
    trend_score: int
    trend_status: str
    message: str
