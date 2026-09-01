from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.dependencies.auth import (
    get_current_user,
)

from app.models.user import User

from app.schemas.payment_reminder import (
    PaymentReminderResponse,
)

from app.services.payment_reminder_service import (
    get_payment_reminders,
)


router = APIRouter(
    prefix="/payment-reminders",
    tags=["Payment Reminders"],
)


@router.get(
    "/",
    response_model=PaymentReminderResponse,
)
def payment_reminders(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    return get_payment_reminders(
        db=db,
        user_id=current_user.id,
    )