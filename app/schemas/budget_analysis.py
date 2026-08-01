from pydantic import BaseModel


class BudgetAnalysisResponse(BaseModel):
    budget_amount: float
    total_spent: float
    remaining_budget: float
    utilization_percentage: float
    status: str
    budget_exceeded: bool
    amount_over_budget: float