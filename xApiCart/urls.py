from django.urls import path, include 
from rest_framework.routers import DefaultRouter 

from xApiCart.views import CartModelViewSet
from xApiCart.views import CartItemModelViewSet
from xApiCart.views import OrderModelViewSet
from xApiCart.views import OrderItemModelViewSet 


router = DefaultRouter() 

router.register(r'cart', CartModelViewSet, basename='cart')
router.register(r'cartitem', CartItemModelViewSet, basename='cartitem')
router.register(r'order', OrderModelViewSet, basename='order')
router.register(r'orderitem', OrderItemModelViewSet, basename='orderitem')


urlpatterns = [
    path('', include(router.urls)),
]




