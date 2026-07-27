from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.services.insight_service import generate_financial_insights

router = APIRouter(
    prefix="/insights",
    tags=["Insights"]
)


@router.get("/summary")
def get_financial_insights(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return generate_financial_insights(
        db=db,
        user_id=current_user.id
    )