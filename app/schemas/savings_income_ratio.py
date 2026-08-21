from pydantic import BaseModel


class SavingsIncomeRatioResponse(BaseModel):
    total_income: float
    total_expense: float
    savings_amount: float
    savings_income_ratio: float
    savings_score: int
    savings_status: str
    message: str
