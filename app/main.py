from fastapi import FastAPI

from app.database.database import engine
import app.database.models
from app.database.database import Base, engine

app = FastAPI(
    title="MoneyMentor AI",
    description="""
    **Spend Smarter. Save Better. Build Your Future.**

    MoneyMentor AI is an AI-powered personal finance and investment platform that helps users manage expenses, create budgets, analyze spending patterns, receive personalized investment recommendations, and achieve long-term financial goals through intelligent insights.
    """,
    version="1.0.0",
)
# Create all database tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {
        "project": "MoneyMentor AI",
        "message": "Application is running successfully.",
        "version": "1.0.0"
    }
