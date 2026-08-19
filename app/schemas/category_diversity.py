from pydantic import BaseModel


class CategoryDiversityResponse(BaseModel):
    total_categories: int
    total_expense: float
    average_expense_per_category: float
    diversity_status: str
    message: str
