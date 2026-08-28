from pydantic import BaseModel


class BudgetRecommendationResponse(BaseModel):
    recommended_budget: float
    basis: str
    message: str