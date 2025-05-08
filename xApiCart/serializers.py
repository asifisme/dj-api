from rest_framework import serializers 

from xApiCart.models import CartModel 
from xApiCart.models import CartItemModel
from xApiCart.models import OrderModel
from xApiCart.models import OrderItemModel 


class CartModelSerializer(serializers.ModelSerializer):
    """
    Serializer for CartModel.
    """
    class Meta:
        model = CartModel
        fields = '__all__'
        read_only_fields = ('id', 'created', 'modified') 


class CartItemModelSerializer(serializers.ModelSerializer):
    """
    Serializer for CartItemModel.
    """
    class Meta:
        model = CartItemModel
        fields = '__all__'
        read_only_fields = ('id', 'created', 'modified') 


class OrderModelSerializer(serializers.ModelSerializer):
    """
    Serializer for OrderModel.
    """
    class Meta:
        model = OrderModel
        fields = '__all__'
        read_only_fields = ('id', 'created', 'modified') 


class OrderItemModelSerializer(serializers.ModelSerializer):
    """
    Serializer for OrderItemModel.
    """
    class Meta:
        model = OrderItemModel
        fields = '__all__'
        read_only_fields = ('id', 'created', 'modified') 