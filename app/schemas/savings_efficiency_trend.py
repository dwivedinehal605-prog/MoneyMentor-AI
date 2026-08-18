from pydantic import BaseModel


class SavingsEfficiencyTrendResponse(BaseModel):
    current_month_savings_rate: float
    previous_month_savings_rate: float
    rate_change: float
    trend: str
    message: str
