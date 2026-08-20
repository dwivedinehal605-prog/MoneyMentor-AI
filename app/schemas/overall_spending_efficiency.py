from pydantic import BaseModel


class OverallSpendingEfficiencyResponse(BaseModel):
    total_income: float
    total_expense: float
    expense_income_ratio: float
    efficiency_score: int
    efficiency_status: str
    message: str
