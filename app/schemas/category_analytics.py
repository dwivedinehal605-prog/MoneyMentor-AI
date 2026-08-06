from pydantic import BaseModel, Field


class CategoryAnalyticsItem(BaseModel):
    """
    Expense summary for a single category.
    """

    category: str = Field(
        ...,
        examples=["Food"],
        description="Expense category."
    )

    total_amount: float = Field(
        ...,
        examples=[8500.00],
        description="Total expense for the category."
    )


class CategoryAnalyticsResponse(BaseModel):
    """
    Category-wise expense analytics.
    """

    categories: list[CategoryAnalyticsItem]

    model_config = {
        "json_schema_extra": {
            "example": {
                "categories": [
                    {
                        "category": "Food",
                        "total_amount": 8500.00
                    },
                    {
                        "category": "Shopping",
                        "total_amount": 12000.00
                    },
                    {
                        "category": "Bills",
                        "total_amount": 5000.00
                    }
                ]
            }
        }
    }