from django.contrib import admin
from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'category', 'date', 'created_at')
    list_filter = ('category', 'date', 'user')
    search_fields = ('user__username', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('user', 'amount', 'category', 'date', 'description')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
