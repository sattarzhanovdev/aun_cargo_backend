from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StockSummaryViewSet, TransactionViewSet
)

router = DefaultRouter()
router.register(r'stocks', StockSummaryViewSet, basename='stock')
router.register(r'transactions', TransactionViewSet, basename='transaction')


urlpatterns = [
    path('', include(router.urls))
]
