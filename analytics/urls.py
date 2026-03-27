from django.urls import path
from .views import AnalyticsViewSet

urlpatterns = [
    path('clustering/', AnalyticsViewSet.as_view({'get': 'clustering'}), name='clustering'),
    path('prediction/', AnalyticsViewSet.as_view({'get': 'prediction'}), name='prediction'),
    path('insights/', AnalyticsViewSet.as_view({'get': 'insights'}), name='insights'),
    path('spending-trends/', AnalyticsViewSet.as_view({'get': 'spending_trends'}), name='spending_trends'),
]
