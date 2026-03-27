from django.contrib import admin
from .models import ExpenseInsight


@admin.register(ExpenseInsight)
class ExpenseInsightAdmin(admin.ModelAdmin):
    list_display = ('user', 'avg_spending', 'last_updated')
    search_fields = ('user__username',)
    readonly_fields = ('last_updated',)
