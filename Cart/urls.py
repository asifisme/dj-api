from django.urls import path, include 
from rest_framework.routers import DefaultRouter 

from .views import CartModelViewSet
from .views import CartItemModelViewSet
from .views import OrderModelViewSet
from .views import OrderItemModelViewSet 


router = DefaultRouter() 

router.register(r'cart', CartModelViewSet, basename='cart')
router.register(r'cartitem', CartItemModelViewSet, basename='cartitem')
router.register(r'order', OrderModelViewSet, basename='order')
router.register(r'orderitem', OrderItemModelViewSet, basename='orderitem')


urlpatterns = [
    path('', include(router.urls)),
]




