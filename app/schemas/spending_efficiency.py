from pydantic import BaseModel


class SpendingEfficiencyResponse(BaseModel):
    current_month_income: float
    current_month_expense: float
    expense_income_ratio: float
    efficiency_score: int
    efficiency_status: str
    message: str
