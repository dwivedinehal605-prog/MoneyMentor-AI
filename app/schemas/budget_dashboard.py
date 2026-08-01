from pydantic import BaseModel


class BudgetDashboardResponse(BaseModel):
    budget_amount: float
    total_spent: float
    remaining_budget: float
    utilization_percentage: float

    status: str

    budget_exceeded: bool
    amount_over_budget: float

    days_remaining: int
    daily_safe_spending: float