from collections import defaultdict

from sklearn.linear_model import LinearRegression
import numpy as np


def train_prediction_model(expenses):
    """
    Train a Linear Regression model using expense amounts.
    """

    if len(expenses) < 2:
        return None

    X = np.array(range(len(expenses))).reshape(-1, 1)
    y = np.array(expenses)

    model = LinearRegression()
    model.fit(X, y)

    return model


def predict_next_expense(model, total_expenses):
    """
    Predict the next expense amount.
    """

    next_index = np.array([[total_expenses]])
    prediction = model.predict(next_index)

    return float(prediction[0])


def predict_monthly_expense(expenses):
    """
    Predict next month's total expense.
    """

    if len(expenses) < 2:
        return None

    monthly_totals = defaultdict(float)

    for expense in expenses:
        month = expense.created_at.strftime("%Y-%m")
        monthly_totals[month] += expense.amount

    totals = list(monthly_totals.values())

    if len(totals) < 2:
        return None

    X = np.arange(len(totals)).reshape(-1, 1)
    y = np.array(totals)

    model = LinearRegression()
    model.fit(X, y)

    prediction = model.predict([[len(totals)]])

    return round(float(prediction[0]), 2)