from pydantic import BaseModel


class CategoryBreakdown(BaseModel):
    category: str
    amount: float


class CategoryInsightResponse(BaseModel):
    highest_spending_category: str
    highest_spending_amount: float

    lowest_spending_category: str
    lowest_spending_amount: float

    total_categories: int

    category_breakdown: list[CategoryBreakdown]