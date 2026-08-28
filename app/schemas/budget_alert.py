from pydantic import BaseModel


class BudgetAlertResponse(BaseModel):
    alert_level: str
    message: str