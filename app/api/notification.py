from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.notification import (
    NotificationResponse,
)

from app.services.notification_service import (
    get_notifications,
)


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


@router.get(
    "",
    response_model=NotificationResponse,
    summary="Get Financial Notifications",
    description=(
        "Returns budget alerts, spending warnings, "
        "large transaction alerts, savings goal progress "
        "updates, and other personalized financial "
        "notifications for the authenticated user."
    ),
    response_description=(
        "List of generated notifications"
    ),
)
def get_notifications_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    return get_notifications(
        db=db,
        user_id=current_user.id,
    )