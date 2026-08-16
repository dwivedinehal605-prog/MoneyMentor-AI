from pydantic import BaseModel


class SpendingDistributionItem(BaseModel):
    category: str
    amount: float
    percentage: float


class SpendingDistributionResponse(BaseModel):
    total_expense: float
    categories: list[SpendingDistributionItem]