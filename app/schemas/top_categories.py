from pydantic import BaseModel, Field


class TopCategory(BaseModel):

    category: str = Field(
        ...,
        examples=["Food"],
    )

    amount: float = Field(
        ...,
        examples=[3500.0],
    )


class TopCategoriesResponse(BaseModel):

    top_categories: list[TopCategory]