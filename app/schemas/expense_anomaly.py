from pydantic import BaseModel, Field


class ExpenseAnomalyItem(BaseModel):
    title: str
    category: str
    amount: float
    average_expense: float
    deviation_percentage: float
    message: str


class ExpenseAnomalyResponse(BaseModel):
    anomaly_detected: bool
    total_expenses_analyzed: int
    anomalies: list[ExpenseAnomalyItem] = Field(
        default_factory=list
    )
    message: str