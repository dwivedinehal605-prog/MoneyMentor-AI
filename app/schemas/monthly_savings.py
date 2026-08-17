from pydantic import BaseModel


class MonthlySavingsResponse(BaseModel):
    current_month_savings: float
    previous_month_savings: float
    change_percentage: float
    trend: str
    message: str