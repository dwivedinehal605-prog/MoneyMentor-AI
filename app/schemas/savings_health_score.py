from pydantic import BaseModel


class SavingsHealthScoreResponse(BaseModel):
    current_month_income: float
    current_month_expense: float
    savings_amount: float
    savings_rate: float
    health_score: int
    financial_status: str
    message: str
