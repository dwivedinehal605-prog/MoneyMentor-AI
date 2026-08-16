from pydantic import BaseModel


class MonthlyComparisonResponse(BaseModel):
    current_month_expense: float
    previous_month_expense: float
    difference: float
    change_percentage: float
    trend: str
    message: str