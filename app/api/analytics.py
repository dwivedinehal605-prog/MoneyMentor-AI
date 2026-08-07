from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.services.analytics_service import (
    get_total_expense,
    category_summary,
)

from app.schemas.category_analytics import (
    CategoryAnalyticsResponse,
)

from app.services.category_analytics_service import (
    get_category_analytics,
)

from app.schemas.category_insight import (
    CategoryInsightResponse,
)

from app.services.category_insight_service import (
    get_category_insights,
)

from app.schemas.monthly_trend import (
    MonthlyTrendResponse,
)

from app.services.monthly_trend_service import (
    get_monthly_trend,
)

from app.services.monthly_trend_service import (
    get_monthly_trend,
)

from app.schemas.top_categories import (
    TopCategoriesResponse,
)

from app.services.top_categories_service import (
    get_top_categories,
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


@router.get(
    "/category-wise",
    response_model=CategoryAnalyticsResponse,
)
def category_wise_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate category-wise
    expense analytics.
    """

    return get_category_analytics(
        db=db,
        user_id=current_user.id,
    )

@router.get(
    "/category-insights",
    response_model=CategoryInsightResponse,
)
def category_insights(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    return get_category_insights(
        db=db,
        user_id=current_user.id,
    )

@router.get(
    "/monthly-trend",
    response_model=MonthlyTrendResponse,
)
def monthly_trend(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Generate month-wise
    expense trend analytics.
    """

    return get_monthly_trend(
        db=db,
        user_id=current_user.id,
    )

@router.get(
    "/top-categories",
    response_model=TopCategoriesResponse,
)
def top_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Return top spending categories.
    """

    return get_top_categories(
        db=db,
        user_id=current_user.id,
    )

print("Analytics router loaded")