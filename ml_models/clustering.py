"""
Clustering module using KMeans algorithm.
Used to identify spending patterns and expense groups.
"""

import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import joblib
import os


MODEL_PATH = os.path.dirname(__file__)


def perform_clustering(X, n_clusters=3, random_state=42):
    """
    Perform KMeans clustering on expense features.
    
    Args:
        X: Feature matrix
        n_clusters: Number of clusters
        random_state: Random seed for reproducibility
    
    Returns:
        clusters: Cluster assignments
        centers: Cluster centers
        silhouette: Silhouette score
    """
    # Ensure X has enough samples
    if len(X) < n_clusters:
        n_clusters = max(2, len(X) - 1)
    
    # Train KMeans
    kmeans = KMeans(
        n_clusters=n_clusters,
        random_state=random_state,
        n_init=10,
        max_iter=300
    )
    
    clusters = kmeans.fit_predict(X)
    centers = kmeans.cluster_centers_
    
    # Calculate silhouette score
    if len(set(clusters)) > 1:
        silhouette = silhouette_score(X, clusters)
    else:
        silhouette = -1.0
    
    # Save model
    save_clustering_model(kmeans, n_clusters)
    
    return clusters, centers, silhouette


def save_clustering_model(model, n_clusters):
    """
    Save clustering model using joblib.
    
    Args:
        model: Trained KMeans model
        n_clusters: Number of clusters
    """
    model_file = os.path.join(MODEL_PATH, 'models', 'kmeans_model.pkl')
    joblib.dump(model, model_file)


def load_clustering_model():
    """
    Load saved clustering model.
    
    Returns:
        Trained KMeans model or None if not found
    """
    model_file = os.path.join(MODEL_PATH, 'models', 'kmeans_model.pkl')
    
    if os.path.exists(model_file):
        return joblib.load(model_file)
    
    return None


def predict_clusters(X):
    """
    Predict clusters for new data using saved model.
    
    Args:
        X: Feature matrix
    
    Returns:
        Cluster predictions
    """
    model = load_clustering_model()
    
    if model is None:
        raise ValueError("No saved clustering model found")
    
    return model.predict(X)


def get_cluster_insights(clusters, expenses):
    """
    Generate insights from clusters.
    
    Args:
        clusters: Cluster assignments
        expenses: List of Expense objects
    
    Returns:
        Dictionary with cluster insights
    """
    insights = {}
    
    for i, (cluster_id, expense) in enumerate(zip(clusters, expenses)):
        if cluster_id not in insights:
            insights[cluster_id] = {
                'count': 0,
                'total': 0,
                'avg': 0,
                'expenses': []
            }
        
        insights[cluster_id]['count'] += 1
        insights[cluster_id]['total'] += float(expense.amount)
        insights[cluster_id]['expenses'].append({
            'id': expense.id,
            'amount': float(expense.amount),
            'category': expense.category,
            'date': expense.date.isoformat()
        })
    
    # Calculate averages
    for cluster_id in insights:
        if insights[cluster_id]['count'] > 0:
            insights[cluster_id]['avg'] = insights[cluster_id]['total'] / insights[cluster_id]['count']
    
    return insights
