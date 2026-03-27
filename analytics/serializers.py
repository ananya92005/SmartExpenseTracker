from rest_framework import serializers
from .models import ExpenseInsight


class ExpenseInsightSerializer(serializers.ModelSerializer):
    """
    Serializer for ExpenseInsight model.
    """
    
    class Meta:
        model = ExpenseInsight
        fields = ['user', 'clustering_data', 'prediction_data', 'avg_spending', 'savings_suggestion', 'last_updated']
        read_only_fields = ['user', 'last_updated']


class ClusteringResultSerializer(serializers.Serializer):
    """
    Serializer for clustering results.
    """
    clusters = serializers.ListField(child=serializers.IntegerField())
    cluster_centers = serializers.ListField(child=serializers.ListField(child=serializers.FloatField()))
    silhouette_score = serializers.FloatField()


class PredictionResultSerializer(serializers.Serializer):
    """
    Serializer for prediction results.
    """
    next_month_prediction = serializers.FloatField()
    next_week_prediction = serializers.FloatField()
    confidence = serializers.FloatField()
