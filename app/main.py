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
app.include_router(report_router)


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