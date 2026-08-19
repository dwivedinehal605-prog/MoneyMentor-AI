from pydantic import BaseModel


class CategoryConcentrationResponse(BaseModel):
    total_expense: float
    top_category: str
    top_category_amount: float
    top_category_percentage: float
    concentration_status: str
    message: str
