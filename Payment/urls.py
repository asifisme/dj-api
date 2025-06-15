from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PaymentViewSet
from .views import  StripeSuccessApiView
from .views import  StripeCancelApiView
from .views import  PayPalPayment 
from .views import PayPalSuccessViewSet


router = DefaultRouter()

router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'paypal', PayPalPayment, basename='paypal-payment') 


urlpatterns = [
    path('paypal/success/', PayPalSuccessViewSet.as_view(), name='paypal-success'),
    # path('paypal/cancel/', PayPalCancelView.as_view(), name='paypal-cancel'),
    path('stripe/success/', StripeSuccessApiView.as_view(), name='stripe-success'),
    path('stripe/cancel/', StripeCancelApiView.as_view(), name='stripe-cancel'),
    path('', include(router.urls)),
]
