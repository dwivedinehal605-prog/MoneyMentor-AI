from pydantic import BaseModel
from typing import List


class GoalAllocation(BaseModel):
    goal: str
    allocation: float


class GoalAllocationResponse(BaseModel):
    monthly_savings_capacity: float
    allocations: List[GoalAllocation]