from pydantic import BaseModel


class GoalPriorityResponse(BaseModel):
    highest_priority_goal: str
    priority_score: int
    reason: str