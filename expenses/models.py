from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ExpenseCategory(models.TextChoices):
    """
    Predefined expense categories.
    """
    FOOD = 'FOOD', 'Food & Dining'
    TRANSPORTATION = 'TRANSPORTATION', 'Transportation'
    UTILITIES = 'UTILITIES', 'Utilities'
    ENTERTAINMENT = 'ENTERTAINMENT', 'Entertainment'
    HEALTHCARE = 'HEALTHCARE', 'Healthcare'
    EDUCATION = 'EDUCATION', 'Education'
    SHOPPING = 'SHOPPING', 'Shopping'
    OTHER = 'OTHER', 'Other'


class Expense(models.Model):
    """
    Expense model to track user expenses.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(
        max_length=20,
        choices=ExpenseCategory.choices,
        default=ExpenseCategory.OTHER
    )
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['user', 'category']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - ${self.amount} ({self.category})"
