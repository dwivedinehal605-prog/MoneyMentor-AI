from pydantic import BaseModel


class CategorySpendingRiskResponse(BaseModel):
    category: str
    current_month_expense: float
    total_expense: float
    expense_percentage: float
    risk_score: int
    risk_status: str
    message: str
