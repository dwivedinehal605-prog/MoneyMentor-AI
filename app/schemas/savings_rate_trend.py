from pydantic import BaseModel


class SavingsRateTrendResponse(BaseModel):
    current_month_savings_rate: float
    previous_month_savings_rate: float
    change_percentage: float
    trend: str
    message: str