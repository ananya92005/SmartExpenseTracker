from rest_framework import serializers
from .models import Expense, ExpenseCategory


class ExpenseSerializer(serializers.ModelSerializer):
    """
    Serializer for Expense model.
    """
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = Expense
        fields = [
            'id', 'user', 'amount', 'category', 'category_display',
            'date', 'description', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class ExpenseCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating expenses.
    """
    
    class Meta:
        model = Expense
        fields = ['amount', 'category', 'date', 'description']
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0.")
        return value


class ExpenseCategorySerializer(serializers.Serializer):
    """
    Serializer for expense categories.
    """
    value = serializers.CharField()
    label = serializers.CharField()


class ExpenseSummarySerializer(serializers.Serializer):
    """
    Serializer for expense summaries.
    """
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
    count = serializers.IntegerField()
    average = serializers.DecimalField(max_digits=10, decimal_places=2)
    by_category = serializers.DictField(child=serializers.DecimalField(max_digits=10, decimal_places=2))
