from pydantic import BaseModel


class ExpenseVolatilityResponse(BaseModel):
    months_analyzed: int
    average_monthly_expense: float
    highest_monthly_expense: float
    lowest_monthly_expense: float
    volatility_percentage: float
    volatility_status: str
    message: str
