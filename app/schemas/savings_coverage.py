from pydantic import BaseModel


class SavingsCoverageResponse(BaseModel):
    total_income: float
    total_expense: float
    savings_amount: float
    coverage_ratio: float
    coverage_score: int
    coverage_status: str
    message: str
