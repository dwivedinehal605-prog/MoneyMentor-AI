from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.dependencies.auth import (
    get_current_user,
)

from app.models.user import User

from app.services.financial_health_service import (
    get_financial_health_score,
)

router = APIRouter(
    prefix="/financial-health",
    tags=["Financial Health"],
)


@router.get("/")
def financial_health(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    return get_financial_health_score(
        db=db,
        user_id=current_user.id,
    )