
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PaymentViewSet
from .views import  StripeSuccessApiView
from .views import  StripeCancelApiView

router = DefaultRouter()

router.register(r'payments', PaymentViewSet, basename='payment')


urlpatterns = [
    path('', include(router.urls)),
    # path('payment-preprocessor/', PaymentPreProssViewSet.as_view(), name='payment-preprocessor'),
    path('stripe/success/', StripeSuccessApiView.as_view(), name='stripe-success'),
    path('stripe/cancel/', StripeCancelApiView.as_view(), name='stripe-cancel'),
]
