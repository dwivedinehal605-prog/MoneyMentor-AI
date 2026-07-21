from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.analytics_service import (
    get_total_expense,
    category_summary,
)

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/total")
def total(db: Session = Depends(get_db)):
    return get_total_expense(db)


@router.get("/category-summary")
def summary(db: Session = Depends(get_db)):
    return category_summary(db)