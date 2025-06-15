from django.urls import path, include 
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

from .views import TrialBalanceViewSet




urlpatterns = [
    path('trial-balance/', TrialBalanceViewSet.as_view(), name='trial-balance-list'),
]
