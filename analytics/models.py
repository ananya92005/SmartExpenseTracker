from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ExpenseInsight(models.Model):
    """
    Stores ML-derived insights for users.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='expense_insight')
    clustering_data = models.JSONField(null=True, blank=True)
    prediction_data = models.JSONField(null=True, blank=True)
    avg_spending = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    savings_suggestion = models.TextField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Expense Insight'
        verbose_name_plural = 'Expense Insights'
    
    def __str__(self):
        return f"Insights for {self.user.username}"
