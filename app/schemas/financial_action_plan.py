from pydantic import BaseModel
from typing import List


class FinancialActionPlanResponse(BaseModel):
    priority: str
    actions: List[str]