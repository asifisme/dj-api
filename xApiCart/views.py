from rest_framework.viewsets import ModelViewSet 
from rest_framework import permissions 



from xApiCart.models import CartModel 
from xApiCart.models import CartItemModel
from xApiCart.models import OrderModel
from xApiCart.models import OrderItemModel  

from xApiCart.serializers import CartModelSerializer
from xApiCart.serializers import CartItemModelSerializer
from xApiCart.serializers import OrderModelSerializer
from xApiCart.serializers import OrderItemModelSerializer 


class CartModelViewSet(ModelViewSet):
    """
    ViewSet for CartModel.
    """
    queryset = CartModel.objects.all()
    serializer_class = CartModelSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'post', 'put', 'delete'] 


class CartItemModelViewSet(ModelViewSet):
    """
    ViewSet for CartItemModel.
    """
    queryset = CartItemModel.objects.all()
    serializer_class = CartItemModelSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'post', 'put', 'delete'] 


class OrderModelViewSet(ModelViewSet):
    """
    ViewSet for OrderModel.
    """
    queryset = OrderModel.objects.all()
    serializer_class = OrderModelSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'post', 'put', 'delete'] 


class OrderItemModelViewSet(ModelViewSet):
    """
    ViewSet for OrderItemModel.
    """
    queryset = OrderItemModel.objects.all()
    serializer_class = OrderItemModelSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'post', 'put', 'delete']