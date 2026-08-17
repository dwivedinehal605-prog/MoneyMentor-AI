from pydantic import BaseModel


class ExpenseFrequencyResponse(BaseModel):
    total_expenses_analyzed: int
    months_analyzed: int
    average_expenses_per_month: float
    most_active_month: str
    highest_monthly_expense_count: int
    frequency_trend: str
    message: str