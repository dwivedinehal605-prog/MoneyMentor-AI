from pydantic import BaseModel


class SpendingInsightResponse(BaseModel):
    highest_category: str
    highest_category_amount: float
    total_expense: float
    percentage_of_total: float
    insight: str