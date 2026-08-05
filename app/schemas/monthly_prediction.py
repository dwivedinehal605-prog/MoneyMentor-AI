from pydantic import BaseModel


class MonthlyPredictionResponse(BaseModel):
    total_income: float
    total_expense: float
    predicted_expense: float
    predicted_savings: float
    savings_status: str
    budget: float
    remaining_budget: float
    forecast: str