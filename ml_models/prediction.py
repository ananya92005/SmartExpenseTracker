"""
Prediction module using Linear Regression.
Used to forecast future expenses.
"""

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import joblib
import os


MODEL_PATH = os.path.dirname(__file__)


def predict_next_month(X, y):
    """
    Predict next month's total expenses using Linear Regression.
    
    Args:
        X: Feature matrix (time-based features)
        y: Target variable (expense amounts)
    
    Returns:
        Predicted total for next month
    """
    # Train model
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict next 30 days
    last_day = X.max()
    next_month_days = np.array([[last_day + i + 1] for i in range(30)])
    
    if X.max() > 0:
        next_month_days = next_month_days / X.max()
    
    predictions = model.predict(next_month_days)
    next_month_total = np.sum(np.maximum(predictions, 0))  # Ensure non-negative
    
    # Save model
    save_prediction_model(model)
    
    return next_month_total


def predict_next_week(X, y):
    """
    Predict next week's total expenses.
    
    Args:
        X: Feature matrix (time-based features)
        y: Target variable (expense amounts)
    
    Returns:
        Predicted total for next week
    """
    # Train model
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict next 7 days
    last_day = X.max()
    next_week_days = np.array([[last_day + i + 1] for i in range(7)])
    
    if X.max() > 0:
        next_week_days = next_week_days / X.max()
    
    predictions = model.predict(next_week_days)
    next_week_total = np.sum(np.maximum(predictions, 0))  # Ensure non-negative
    
    return next_week_total


def save_prediction_model(model):
    """
    Save prediction model using joblib.
    
    Args:
        model: Trained LinearRegression model
    """
    model_file = os.path.join(MODEL_PATH, 'models', 'regression_model.pkl')
    joblib.dump(model, model_file)


def load_prediction_model():
    """
    Load saved prediction model.
    
    Returns:
        Trained LinearRegression model or None if not found
    """
    model_file = os.path.join(MODEL_PATH, 'models', 'regression_model.pkl')
    
    if os.path.exists(model_file):
        return joblib.load(model_file)
    
    return None


def predict_daily_average(X, y):
    """
    Predict average daily expenses.
    
    Args:
        X: Feature matrix (time-based features)
        y: Target variable (expense amounts)
    
    Returns:
        Average daily expense prediction
    """
    model = LinearRegression()
    model.fit(X, y)
    
    avg_prediction = np.mean(model.predict(X))
    return max(avg_prediction, 0)  # Ensure non-negative


def get_model_confidence(X, y):
    """
    Get confidence score (R-squared) of the prediction model.
    
    Args:
        X: Feature matrix
        y: Target variable
    
    Returns:
        R-squared score
    """
    model = LinearRegression()
    model.fit(X, y)
    
    return model.score(X, y)
