from rest_framework import serializers 
from django.shortcuts import get_object_or_404 
from decimal import Decimal

from .models import CartModel 
from .models import CartItemModel
from .models import OrderModel
from .models import OrderItemModel 

from Product.models import ProductModel 


class CartModelSerializer(serializers.ModelSerializer):
    """
    Serializer for CartModel.
    """
    class Meta:
        model = CartModel
        fields = [ 'id','author', 'uid', 'created', 'modified'] 
        read_only_fields = ('id', 'author', 'uid', 'created', 'modified') 



class CartItemModelSerializer(serializers.ModelSerializer):
    """
    Serializer for CartItemModel.
    """
    # author = serializers.StringRelatedField(source='cart_id.author', read_only=True)
    product_uid = serializers.CharField(write_only=True, required=False)
    quantity = serializers.IntegerField(default=1)

    class Meta:
        model = CartItemModel
        fields = ['id', 'cart_id', 'product_uid', 'quantity', 'product_id', 'price', 'is_active', 'uid', 'created', 'modified']
        read_only_fields = ('id', 'cart_id', 'product_id', 'uid', 'price', 'created', 'modified') 

    def validate_quantity(self, value):
        """
        Validate that the quantity is a positive integer.
        """
        if value < 0:
            raise serializers.ValidationError("Quantity must be zero or positive.")
        return value 

    

class OrderModelSerializer(serializers.ModelSerializer):
    """
    Serializer for OrderModel.
    """
    
    class Meta:
        model = OrderModel
        fields = [ "id", "author", "cart_id", "order_num", "order_note", "ord_status", "total_amount", "payment_status", "shipping_status", "is_confirmed", "uid", "created", "modified"]
        read_only_fields = [ "id", "author","cart_id", "order_num", "order_note", "ord_status", "total_amount", "payment_status","shipping_status", "uid", "created", "modified"]



class OrderItemModelSerializer(serializers.ModelSerializer):
    """
    Serializer for OrderItemModel.
    """
    class Meta:
        model = OrderItemModel
        fields = ['id', 'uid', 'order_id', 'product_id', 'price', 'quantity', 'created', 'modified']
        read_only_fields = ('id', 'uid', 'price', 'created', 'modified')