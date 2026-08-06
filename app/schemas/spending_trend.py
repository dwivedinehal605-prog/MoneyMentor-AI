from pydantic import BaseModel, Field


class SpendingTrendResponse(BaseModel):
    """
    Response schema for spending trend analysis.
    """

    trend: str = Field(
        ...,
        examples=["Increasing"],
        description="Overall monthly spending trend."
    )

    change_percentage: float = Field(
        ...,
        examples=[18.75],
        description="Percentage increase or decrease compared to the previous month."
    )

    current_month_expense: float = Field(
        ...,
        examples=[15000.00],
        description="Total expense for the current month."
    )

    previous_month_expense: float = Field(
        ...,
        examples=[12600.00],
        description="Total expense for the previous month."
    )