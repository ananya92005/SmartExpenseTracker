from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

from .models import ExpenseInsight
from .serializers import (
    ExpenseInsightSerializer,
    ClusteringResultSerializer,
    PredictionResultSerializer
)
from ml_models.clustering import perform_clustering
from ml_models.prediction import predict_next_month, predict_next_week
from ml_models.preprocessing import prepare_expense_data

User = get_user_model()


class AnalyticsViewSet(viewsets.ViewSet):
    """
    ViewSet for analytics and ML predictions.
    """
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def clustering(self, request):
        """
        Perform KMeans clustering on user expenses.
        """
        try:
            expenses = request.user.expenses.all()
            
            if expenses.count() < 3:
                return Response(
                    {'error': 'Need at least 3 expenses for clustering'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Prepare data
            X, expense_ids = prepare_expense_data(expenses)
            
            # Perform clustering
            clusters, centers, silhouette = perform_clustering(X, n_clusters=min(3, len(set(expenses.values_list('category', flat=True)))))
            
            # Store results
            insight, _ = ExpenseInsight.objects.get_or_create(user=request.user)
            insight.clustering_data = {
                'clusters': clusters.tolist(),
                'centers': centers.tolist(),
                'silhouette_score': float(silhouette)
            }
            insight.save()
            
            return Response({
                'clusters': clusters.tolist(),
                'silhouette_score': float(silhouette),
                'interpretation': 'Expenses grouped into spending patterns. Higher silhouette score indicates better separation.'
            })
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def prediction(self, request):
        """
        Predict next month's expenses using Linear Regression.
        """
        try:
            expenses = request.user.expenses.all()
            
            if expenses.count() < 7:
                return Response(
                    {'error': 'Need at least 7 expenses for prediction'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Prepare data
            X, y = prepare_expense_data(expenses, for_prediction=True)
            
            # Predict
            next_month = predict_next_month(X, y)
            next_week = predict_next_week(X, y)
            
            # Calculate confidence (R-squared)
            from sklearn.linear_model import LinearRegression
            model = LinearRegression()
            model.fit(X, y)
            confidence = model.score(X, y)
            
            # Store results
            insight, _ = ExpenseInsight.objects.get_or_create(user=request.user)
            insight.prediction_data = {
                'next_month': float(next_month),
                'next_week': float(next_week),
                'confidence': float(confidence)
            }
            insight.save()
            
            return Response({
                'next_month_prediction': float(next_month),
                'next_week_prediction': float(next_week),
                'confidence': float(confidence),
                'interpretation': 'Based on historical spending patterns using Linear Regression.'
            })
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def insights(self, request):
        """
        Get comprehensive insights and suggestions.
        """
        try:
            expenses = request.user.expenses.all()
            
            if expenses.count() == 0:
                return Response({
                    'message': 'No expenses recorded yet',
                    'suggestions': ['Start tracking your expenses to get insights']
                })
            
            from django.db.models import Sum, Avg
            from expenses.models import ExpenseCategory
            
            # Calculate statistics
            total_spending = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
            avg_spending = expenses.aggregate(Avg('amount'))['amount__avg'] or 0
            
            # Category analysis
            category_spending = {}
            for category in ExpenseCategory:
                cat_amount = expenses.filter(
                    category=category[0]
                ).aggregate(Sum('amount'))['amount__sum'] or 0
                if cat_amount > 0:
                    category_spending[category[1]] = float(cat_amount)
            
            # Get highest spending category
            highest_category = max(category_spending, key=category_spending.get) if category_spending else None
            highest_amount = category_spending.get(highest_category, 0) if highest_category else 0
            
            # Generate suggestions
            suggestions = self._generate_suggestions(
                total_spending, avg_spending, category_spending, highest_category, highest_amount
            )
            
            # Store insights
            insight, _ = ExpenseInsight.objects.get_or_create(user=request.user)
            insight.avg_spending = avg_spending
            insight.savings_suggestion = suggestions[0] if suggestions else 'Keep tracking your expenses'
            insight.save()
            
            return Response({
                'total_spending': float(total_spending),
                'average_expense': float(avg_spending),
                'highest_category': highest_category,
                'highest_category_amount': highest_amount,
                'category_breakdown': category_spending,
                'suggestions': suggestions
            })
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def spending_trends(self, request):
        """
        Get spending trends over the last 30 days.
        """
        try:
            expenses = request.user.expenses.all()
            
            today = datetime.now().date()
            thirty_days_ago = today - timedelta(days=30)
            
            recent_expenses = expenses.filter(date__gte=thirty_days_ago, date__lte=today)
            
            # Daily spending
            daily_spending = {}
            for i in range(30):
                date = thirty_days_ago + timedelta(days=i)
                from django.db.models import Sum
                amount = recent_expenses.filter(date=date).aggregate(Sum('amount'))['amount__sum'] or 0
                daily_spending[date.isoformat()] = float(amount)
            
            # Weekly spending
            weekly_spending = []
            for i in range(4):
                week_start = thirty_days_ago + timedelta(days=i*7)
                week_end = week_start + timedelta(days=6)
                from django.db.models import Sum
                amount = recent_expenses.filter(
                    date__gte=week_start, date__lte=week_end
                ).aggregate(Sum('amount'))['amount__sum'] or 0
                weekly_spending.append({
                    'week': f"Week {i+1}",
                    'total': float(amount)
                })
            
            return Response({
                'daily_spending': daily_spending,
                'weekly_spending': weekly_spending
            })
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @staticmethod
    def _generate_suggestions(total_spending, avg_spending, category_spending, highest_category, highest_amount):
        """
        Generate personalized suggestions based on spending patterns.
        """
        suggestions = []
        
        # High spending suggestions
        if highest_category and highest_amount > avg_spending * 3:
            suggestions.append(
                f"Your {highest_category.lower()} spending (${highest_amount:.2f}) is significantly higher than average. "
                f"Consider setting a budget for this category."
            )
        
        # Savings suggestions
        if total_spending > 0:
            avg_daily = float(total_spending) / 30
            if avg_daily > 50:
                suggestions.append(
                    f"Your average daily spending is ${avg_daily:.2f}. Try to reduce this by 10-15% by cutting unnecessary expenses."
                )
        
        if not suggestions:
            suggestions.append("Your spending looks balanced. Keep up the good habit!")
        
        return suggestions
