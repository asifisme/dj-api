
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, StripeSuccessApiView, StripeCancelApiView

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
    path('stripe/success/', StripeSuccessApiView.as_view(), name='stripe-success'),
    path('stripe/cancel/', StripeCancelApiView.as_view(), name='stripe-cancel'),
]
