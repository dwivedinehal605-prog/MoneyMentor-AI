from fastapi import FastAPI
from app.api.expense import router as expense_router

from app.database.database import Base, engine

app = FastAPI(
    title="MoneyMentor AI",
    description="""
    **Spend Smarter. Save Better. Build Your Future.**

    MoneyMentor AI is an AI-powered personal finance and investment platform that helps users manage expenses, create budgets, analyze spending patterns, receive personalized investment recommendations, and achieve long-term financial goals through intelligent insights.
    """,
    version="1.0.0",
)
app.include_router(expense_router)
# Create all database tables
Base.metadata.create_all(bind=engine)

@app.get("/", tags=["Home"])
def home():
    return {
        "message": "MoneyMentor AI Backend is running."
    }
