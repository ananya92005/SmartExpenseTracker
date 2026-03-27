from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from django.db.models import Sum, Count, Avg
from datetime import datetime, timedelta

from .models import Expense, ExpenseCategory
from .serializers import (
    ExpenseSerializer,
    ExpenseCreateSerializer,
    ExpenseCategorySerializer,
    ExpenseSummarySerializer
)


class ExpenseFilter(filters.FilterSet):
    """
    Filter for Expense model.
    """
    date_from = filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = filters.DateFilter(field_name='date', lookup_expr='lte')
    
    class Meta:
        model = Expense
        fields = ['category', 'date_from', 'date_to']


class ExpenseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Expense operations.
    Provides CRUD operations and filtering capabilities.
    """
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = ExpenseFilter
    ordering_fields = ['date', 'amount', 'created_at']
    ordering = ['-date']
    
    def get_queryset(self):
        """
        Return expenses for the current user only.
        """
        return Expense.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """
        Use specific serializer based on action.
        """
        if self.action in ['create', 'update', 'partial_update']:
            return ExpenseCreateSerializer
        return ExpenseSerializer
    
    def perform_create(self, serializer):
        """
        Create expense for the current user.
        """
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def categories(self, request):
        """
        Get all available expense categories.
        """
        categories = [
            {'value': choice[0], 'label': choice[1]}
            for choice in ExpenseCategory.choices
        ]
        return Response(categories)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Get expense summary for current month and all months.
        """
        expenses = self.get_queryset()
        
        # Overall summary
        total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        count = expenses.count()
        average = expenses.aggregate(Avg('amount'))['amount__avg'] or 0
        
        # By category
        by_category = {}
        for category in ExpenseCategory:
            amount = expenses.filter(
                category=category[0]
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            if amount > 0:
                by_category[category[1]] = float(amount)
        
        data = {
            'total': float(total),
            'count': count,
            'average': float(average),
            'by_category': by_category
        }
        
        return Response(data)
    
    @action(detail=False, methods=['get'])
    def monthly_summary(self, request):
        """
        Get monthly expense summary.
        """
        expenses = self.get_queryset()
        
        # Current month
        today = datetime.now().date()
        first_day = today.replace(day=1)
        last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        current_month_expenses = expenses.filter(date__gte=first_day, date__lte=last_day)
        current_month_total = current_month_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Previous months (last 12 months)
        monthly_data = []
        for i in range(11, -1, -1):
            month_date = today - timedelta(days=30*i)
            month_first = month_date.replace(day=1)
            month_last = (month_first + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            
            month_total = expenses.filter(
                date__gte=month_first,
                date__lte=month_last
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            
            monthly_data.append({
                'month': month_first.strftime('%B %Y'),
                'total': float(month_total)
            })
        
        return Response({
            'current_month_total': float(current_month_total),
            'monthly_data': monthly_data
        })
    
    @action(detail=False, methods=['get'])
    def category_summary(self, request):
        """
        Get category-wise expense breakdown.
        """
        expenses = self.get_queryset()
        
        category_data = {}
        for category in ExpenseCategory:
            expenses_in_category = expenses.filter(category=category[0])
            total = expenses_in_category.aggregate(Sum('amount'))['amount__sum'] or 0
            count = expenses_in_category.count()
            average = expenses_in_category.aggregate(Avg('amount'))['amount__avg'] or 0
            
            if total > 0:
                category_data[category[1]] = {
                    'total': float(total),
                    'count': count,
                    'average': float(average)
                }
        
        return Response(category_data)
