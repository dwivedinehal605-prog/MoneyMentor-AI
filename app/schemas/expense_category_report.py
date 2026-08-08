from pydantic import BaseModel
from pydantic import Field


class CategoryExpense(BaseModel):

    category: str = Field(
        ...,
        examples=["Food"],
    )

    amount: float = Field(
        ...,
        examples=[3500.0],
    )


class ExpenseCategoryReportResponse(
    BaseModel
):

    total_categories: int

    categories: list[
        CategoryExpense
    ]