"""
Data preprocessing module for expense data.
Handles feature engineering and data preparation for ML models.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


def prepare_expense_data(expenses, for_prediction=False):
    """
    Prepare expense data for ML models.
    
    Args:
        expenses: QuerySet of Expense objects
        for_prediction: Boolean indicating if data is for prediction
    
    Returns:
        X: Feature matrix
        y: Target variable (if for_prediction), or expense_ids
    """
    if for_prediction:
        return _prepare_prediction_data(expenses)
    else:
        return _prepare_clustering_data(expenses)


def _prepare_clustering_data(expenses):
    """
    Prepare data for clustering analysis.
    
    Returns:
        X: Feature matrix [amount, day_of_week, day_of_month, days_since_expense]
        expense_ids: IDs for tracking
    """
    data = []
    expense_ids = []
    
    today = datetime.now().date()
    
    for expense in expenses:
        # Calculate features
        amount = float(expense.amount)
        day_of_week = expense.date.weekday()
        day_of_month = expense.date.day
        days_since = (today - expense.date).days
        
        data.append([amount, day_of_week, day_of_month, days_since])
        expense_ids.append(expense.id)
    
    X = np.array(data)
    
    # Normalization
    X = normalize_features(X)
    
    return X, expense_ids


def _prepare_prediction_data(expenses):
    """
    Prepare data for prediction models.
    
    Returns:
        X: Time-based features [days_elapsed]
        y: Expense amounts
    """
    # Get expenses sorted by date
    expenses_sorted = expenses.order_by('date').values('date', 'amount')
    
    if len(expenses_sorted) < 2:
        raise ValueError("Need at least 2 expenses for prediction")
    
    first_date = expenses_sorted.first()['date']
    
    X = []
    y = []
    
    for expense in expenses_sorted:
        days_elapsed = (expense['date'] - first_date).days
        X.append([days_elapsed])
        y.append(float(expense['amount']))
    
    X = np.array(X)
    y = np.array(y)
    
    # Normalize X
    if X.max() > 0:
        X = X / X.max()
    
    return X, y


def normalize_features(X):
    """
    Normalize features using mean-std normalization.
    
    Args:
        X: Feature matrix
    
    Returns:
        X_normalized: Normalized feature matrix
    """
    X = X.astype(float)
    
    for i in range(X.shape[1]):
        col = X[:, i]
        mean = np.mean(col)
        std = np.std(col)
        
        if std > 0:
            X[:, i] = (col - mean) / std
        else:
            X[:, i] = col - mean
    
    return X


def create_time_series_features(expenses):
    """
    Create time-series features for temporal analysis.
    
    Args:
        expenses: QuerySet of Expense objects
    
    Returns:
        DataFrame with time-series features
    """
    data = []
    
    for expense in expenses:
        data.append({
            'date': expense.date,
            'amount': float(expense.amount),
            'category': expense.category,
            'day_of_week': expense.date.weekday(),
            'week_of_year': expense.date.isocalendar()[1],
            'month': expense.date.month,
            'year': expense.date.year,
        })
    
    df = pd.DataFrame(data)
    return df.sort_values('date')
