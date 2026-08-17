from pydantic import BaseModel


class ExpenseHealthScoreResponse(BaseModel):
    current_month_income: float
    current_month_expense: float
    expense_income_ratio: float
    health_score: int
    financial_status: str
    message: str