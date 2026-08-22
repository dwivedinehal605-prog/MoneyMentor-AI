
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.income_expense_report import (
    IncomeExpenseReportResponse,
)
from app.schemas.category_analytics import (
    CategoryAnalyticsResponse,
)
from app.schemas.category_insight import (
    CategoryInsightResponse,
)
from app.schemas.monthly_trend import (
    MonthlyTrendResponse,
)
from app.schemas.top_categories import (
    TopCategoriesResponse,
)
from app.schemas.monthly_report import (
    MonthlyReportResponse,
)
from app.schemas.savings_summary import (
    SavingsSummaryResponse,
)
from app.schemas.financial_health_report import (
    FinancialHealthReportResponse,
)
from app.schemas.expense_category_report import (
    ExpenseCategoryReportResponse,
)

from app.services.analytics_service import (
    get_total_expense,
    category_summary,
)
from app.services.category_analytics_service import (
    get_category_analytics,
)
from app.services.category_insight_service import (
    get_category_insights,
)
from app.services.monthly_trend_service import (
    get_monthly_trend,
)
from app.services.top_categories_service import (
    get_top_categories,
)
from app.services.monthly_report_service import (
    get_monthly_report,
)
from app.services.income_expense_report_service import (
    get_income_expense_report,
)
from app.services.savings_summary_service import (
    get_savings_summary,
)
from app.services.financial_health_report_service import (
    get_financial_health_report,
)
from app.services.expense_category_report_service import (
    get_expense_category_report,
)


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get("/total")
def total(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_total_expense(
        db=db,
        user_id=current_user.id,
    )


@router.get("/category-summary")
def summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return category_summary(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/category-wise",
    response_model=CategoryAnalyticsResponse,
)
def category_wise_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate category-wise expense analytics.
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
    current_user: User = Depends(get_current_user),
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
    current_user: User = Depends(get_current_user),
):
    """
    Generate month-wise expense trend analytics.
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
    current_user: User = Depends(get_current_user),
):
    """
    Return top spending categories.
    """

    return get_top_categories(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/monthly-report",
    response_model=MonthlyReportResponse,
)
def monthly_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_monthly_report(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/income-expense-report",
    response_model=IncomeExpenseReportResponse,
)
def income_expense_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_income_expense_report(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/savings-summary",
    response_model=SavingsSummaryResponse,
)
def savings_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_savings_summary(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/financial-health-report",
    response_model=FinancialHealthReportResponse,
)
def financial_health_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_financial_health_report(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/expense-category-report",
    response_model=ExpenseCategoryReportResponse,
)
def expense_category_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_expense_category_report(
        db=db,
        user_id=current_user.id,
    )