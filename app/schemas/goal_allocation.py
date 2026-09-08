from pydantic import BaseModel


class GoalAllocationItem(BaseModel):
    goal: str
    remaining_amount: float
    monthly_required: float
    recommended_allocation: float
    funding_status: str


class GoalAllocationResponse(BaseModel):
    monthly_savings_capacity: float
    total_allocated: float
    remaining_capacity: float
    allocations: list[GoalAllocationItem]