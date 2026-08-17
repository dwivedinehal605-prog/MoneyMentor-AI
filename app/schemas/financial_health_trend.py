from pydantic import BaseModel


class FinancialHealthTrendResponse(BaseModel):
    current_month_score: int
    previous_month_score: int
    score_change: int
    trend: str
    message: str
