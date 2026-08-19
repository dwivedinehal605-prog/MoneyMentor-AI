from pydantic import BaseModel


class MonthlyCategoryTrendResponse(BaseModel):
    category: str
    current_month_expense: float
    previous_month_expense: float
    change_percentage: float
    trend: str
    message: str
