from pydantic import BaseModel, Field


class MonthlyTrendResponse(BaseModel):
    """
    Monthly expense trend response.
    """

    months: list[str] = Field(
        ...,
        examples=[["2026-05", "2026-06", "2026-07"]],
        description="Months in chronological order."
    )

    expenses: list[float] = Field(
        ...,
        examples=[[5000.0, 7200.0, 6500.0]],
        description="Total expense for each month."
    )