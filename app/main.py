from fastapi import FastAPI

# Routers
from app.api.user import router as user_router
from app.api.expense import router as expense_router
from app.api.income import router as income_router
from app.api.analytics import router as analytics_router
from app.api.insights import router as insights_router
from app.api.prediction import router as prediction_router
from app.api.dashboard import router as dashboard_router
from app.api.budget import router as budget_router
from app.api.savings_goal import router as savings_goal_router
from app.api.recommendation import router as recommendation_router
from app.api.report import router as report_router
from app.api.chart import router as chart_router
from app.api.notification import router as notification_router
from app.api.anomaly import router as anomaly_router
from app.api.spending_insight import router as spending_insight_router
from app.api.spending_distribution import router as spending_distribution_router
from app.api.monthly_comparison import router as monthly_comparison_router
from app.api.savings_rate_trend import router as savings_rate_trend_router
from app.api.expense_frequency import router as expense_frequency_router
from app.api.category_concentration import router as category_concentration_router
from app.api.category_diversity import router as category_diversity_router
from app.api.monthly_category_trend import router as monthly_category_trend_router
from app.api.category_trend_score import router as category_trend_score_router
from app.api.category_spending_risk import router as category_spending_risk_router
from app.api.overall_spending_risk import router as overall_spending_risk_router
from app.api.overall_spending_efficiency import router as overall_spending_efficiency_router
from app.api.expense_income_balance import router as expense_income_balance_router
from app.api.expense_income_ratio import router as expense_income_ratio_router
from app.api.monthly_savings import router as monthly_savings_router
from app.api.expense_health_score import router as expense_health_score_router
from app.api.financial_health_trend import router as financial_health_trend_router
from app.api.savings_health_score import router as savings_health_score_router
from app.api.spending_efficiency import router as spending_efficiency_router
from app.api.savings_efficiency_trend import router as savings_efficiency_trend_router
from app.api.expense_volatility import router as expense_volatility_router

# Database
from app.database.database import Base, engine

# Models
from app.models.user import User
from app.models.expense import Expense
from app.models.income import Income
from app.models.budget import Budget
from app.models.savings_goal import SavingsGoal

app = FastAPI(
    title="MoneyMentor AI",
    description="""
# 💰 MoneyMentor AI

Spend Smarter. Save Better. Build Your Future.

MoneyMentor AI is an AI-powered personal finance management platform that helps users:

- Track Expenses
- Manage Income
- Analyze Financial Health
- Create Monthly Budgets
- Track Savings Goals
- View Dashboard Analytics
- Receive AI-Powered Financial Recommendations
""",
    version="1.0.0",
)

# ==========================
# Register Routers
# ==========================

app.include_router(user_router)
app.include_router(expense_router)
app.include_router(income_router)
app.include_router(analytics_router)
app.include_router(insights_router)
app.include_router(prediction_router)
app.include_router(dashboard_router)
app.include_router(budget_router)
app.include_router(savings_goal_router)
app.include_router(recommendation_router)
app.include_router(report_router)
app.include_router(chart_router)
app.include_router(notification_router)
app.include_router(anomaly_router)
app.include_router(spending_insight_router)
app.include_router(spending_distribution_router)
app.include_router(monthly_comparison_router)
app.include_router(savings_rate_trend_router )
app.include_router(savings_rate_trend_router)
app.include_router(expense_frequency_router)
app.include_router(expense_income_ratio_router)
app.include_router(monthly_savings_router)
app.include_router(expense_health_score_router)
app.include_router(financial_health_trend_router)
app.include_router(savings_health_score_router)
app.include_router(spending_efficiency_router)
app.include_router(savings_efficiency_trend_router)
app.include_router(expense_volatility_router)
app.include_router(category_concentration_router)
app.include_router(category_diversity_router)
app.include_router(monthly_category_trend_router)
app.include_router(category_trend_score_router)
app.include_router(category_spending_risk_router)
app.include_router(overall_spending_risk_router)
app.include_router(overall_spending_efficiency_router)
app.include_router(expense_income_balance_router)

# ==========================
# Create Database Tables
# ==========================

Base.metadata.create_all(bind=engine)

# ==========================
# Home Endpoint
# ==========================

@app.get("/", tags=["Home"])
def home():
    return {
        "message": "MoneyMentor AI Backend is running successfully."
    }
