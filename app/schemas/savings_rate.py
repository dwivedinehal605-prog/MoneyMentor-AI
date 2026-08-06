from pydantic import BaseModel, Field


class SavingsRateResponse(BaseModel):
    """
    Response schema for savings
    rate analysis.
    """

    total_income: float = Field(
        ...,
        examples=[50000.00],
    )

    total_expense: float = Field(
        ...,
        examples=[32000.00],
    )

    total_savings: float = Field(
        ...,
        examples=[18000.00],
    )

    savings_rate: float = Field(
        ...,
        examples=[36.0],
        description="Percentage of income saved."
    )

    financial_status: str = Field(
        ...,
        examples=["Healthy"],
    )