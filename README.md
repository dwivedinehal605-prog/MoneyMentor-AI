# MoneyMentor AI

# Tagline

**Spend Smarter. Save Better. Build Your Future.**

# Overview

MoneyMentor AI is a personal finance management platform that helps users track income, manage expenses, create budgets, monitor savings goals, and gain actionable financial insights.

The application provides a secure and scalable backend built with FastAPI and SQLAlchemy, along with advanced analytics features that help users understand spending behavior and improve financial planning.

# Features

# Authentication & Security

- User Registration
- Secure Login System
- JWT Authentication
- Protected Routes
- User Data Isolation

# Expense Management

- Add Expenses
- Update Expenses
- Delete Expenses
- View Expense History
- Category-Based Tracking

# Income Management

- Add Income Sources
- Update Income Records
- Delete Income Records
- Income History

# Analytics & Insights

- Total Income Analysis
- Total Expense Analysis
- Savings Calculation
- Category-Wise Spending Analysis
- Monthly Financial Trends
- Top Spending Categories
- Financial Health Report

# Budget Management

- Create Monthly Budgets
- Update Budgets
- Budget Dashboard
- Budget Utilization Analysis
- Over-Budget Detection

# Savings Goals

- Create Savings Goals
- Track Goal Progress
- Goal Dashboard
- Goal Completion Monitoring

# Smart Goal Allocation

- Goal Prioritization System
- Monthly Savings Allocation Recommendations
- Funding Status Analysis
- Deadline-Based Goal Scoring

# Financial Dashboard

- Income Summary
- Expense Summary
- Savings Overview
- Financial Health Score
- Spending Distribution
- Recent Transactions
- Largest Expense Tracking

# Tech Stack

# Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- JWT Authentication

# Database

- SQLite

# Testing

- Pytest
- TestClient

# API Documentation

- Swagger UI
- OpenAPI

# Frontend (Planned)

- React
- TypeScript
- Tailwind CSS
- ShadCN UI
- Recharts
- Framer Motion

# Project Structure

```text
MoneyMentor-AI/
│
├── app/
│   ├── api/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── dependencies/
│   ├── database/
│   └── utils/
│
├── tests/
│
├── requirements.txt
├── main.py
└── README.md
```

# Installation

# Clone Repository

```bash
git clone https://github.com/your-username/MoneyMentor-AI.git
cd MoneyMentor-AI
```

# Create Virtual Environment

```bash
python -m venv venv
```

# Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

# Install Dependencies

```bash
pip install -r requirements.txt
```

# Run Server

```bash
uvicorn app.main:app --reload
```

Server:

```text
http://127.0.0.1:8000
```

Swagger Docs:

```text
http://127.0.0.1:8000/docs
```

# Authentication

MoneyMentor AI uses JWT (JSON Web Token) authentication.

# Register

```http
POST /users/register
```

# Login

```http
POST /users/login
```

# Current User

```http
GET /users/me
```

All protected endpoints require:

```text
Authorization: Bearer <access_token>
```

# API Endpoints

# Users

```http
POST   /users/register
POST   /users/login
GET    /users/me
```

# Expenses

```http
GET    /expenses
POST   /expenses
PUT    /expenses/{id}
DELETE /expenses/{id}
```

# Income

```http
GET    /income
GET    /income/{id}
POST   /income
PUT    /income/{id}
DELETE /income/{id}
```

# Budgets

```http
GET    /budgets
GET    /budgets/current
POST   /budgets
PUT    /budgets/{id}
DELETE /budgets/{id}
```

# Analytics

```http
GET    /analytics/total
GET    /analytics/category-summary
GET    /analytics/monthly-trend
GET    /analytics/top-categories
GET    /analytics/monthly-report
GET    /analytics/financial-health
```

# Dashboard

```http
GET    /dashboard/summary
```

# Savings Goals

```http
GET    /goals
GET    /goals/{id}
POST   /goals
PUT    /goals/{id}
DELETE /goals/{id}
GET    /goals/{id}/progress
GET    /goals/dashboard
```

# Testing

The project includes comprehensive automated testing.

# Run Tests

```bash
pytest -v
```

# Current Status

```text
70 Tests Passed ✅
0 Failures ✅
```

Coverage Includes:

- Authentication
- Expenses
- Income
- Budgets
- Analytics
- Dashboard
- Savings Goals
- Goal Allocation
- User Isolation
- Authorization

# Project Highlights

- RESTful API Architecture
- JWT Authentication
- Service-Based Design Pattern
- SQLAlchemy ORM
- Automated Testing
- Financial Analytics
- Goal Allocation Engine
- Interactive Dashboard
- Clean Modular Structure

# Future Improvements

- React Frontend
- PostgreSQL Integration
- Docker Support
- AI-Powered Financial Recommendations
- Email Notifications
- Expense Forecasting
- OCR Receipt Scanner
- Mobile Application
- Cloud Deployment

# Author

Nehal Dwivedi

B.Tech Computer Science Engineering (2023–2027)

Shambhunath Institute of Engineering and Technology

Prayagraj, India