from fastapi import FastAPI

from app.api.expense import router as expense_router
from app.api.user import router as user_router
from app.api.income import router as income_router

from app.database.database import Base, engine

# Import models so SQLAlchemy knows about them
from app.models.expense import Expense
from app.models.user import User
from app.models.income import Income

app = FastAPI(
    title="MoneyMentor AI",
    description="""
    **Spend Smarter. Save Better. Build Your Future.**

    MoneyMentor AI is an AI-powered personal finance and investment platform that helps users manage expenses, create budgets, analyze spending patterns, receive personalized investment recommendations, and achieve long-term financial goals through intelligent insights.
    """,
    version="1.0.0",
)

# Register Routers
app.include_router(expense_router)
app.include_router(user_router)
app.include_router(income_router)

# Create Database Tables
Base.metadata.create_all(bind=engine)


@app.get("/", tags=["Home"])
def home():
    return {
        "message": "MoneyMentor AI Backend is running."
    }