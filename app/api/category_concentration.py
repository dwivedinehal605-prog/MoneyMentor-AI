from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.category_concentration import (
    CategoryConcentrationResponse,
)

from app.services.category_concentration_service import (
    get_category_concentration,
)


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get(
    "/category-concentration",
    response_model=CategoryConcentrationResponse,
)
def category_concentration(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Analyze spending concentration
    in the top expense category.
    """

    return get_category_concentration(
        db=db,
        user_id=current_user.id,
    )
