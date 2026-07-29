from pydantic import BaseModel


class FinancialInsightResponse(BaseModel):
    total_income: float
    total_expense: float
    savings: float
    savings_rate: float
    highest_spending_category: str

    financial_health_score: int
    health_status: str

    monthly_trend: str
    previous_month_expense: float
    current_month_expense: float

    insight: str