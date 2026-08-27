from pydantic import BaseModel


class BudgetPerformanceResponse(BaseModel):
    budget: float
    spent: float
    remaining: float
    utilization_percentage: float
    status: str