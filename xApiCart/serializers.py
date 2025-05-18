from rest_framework import serializers 
from django.shortcuts import get_object_or_404 

from .models import CartModel 
from .models import CartItemModel
from .models import OrderModel
from .models import OrderItemModel 

from xApiProduct.models import ProductModel 


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
    author = serializers.StringRelatedField(source='cart_id.author', read_only=True)
    product_uid = serializers.CharField(write_only=True )

    class Meta:
        model = CartItemModel
        fields = ['id', 'author', 'cart_id', 'product_uid', 'quantity', 'price', 'is_active', 'uid', 'created', 'modified']
        read_only_fields = ('id', 'uid', 'price', 'created', 'modified') 

    
    def get_product(self, obj):
        return {
            "name" : obj.product_id.name, 
            "uid" : obj.product_id.uid
        }
    
    def create(self, validated_data):
        product_uid = validated_data.pop('product_uid')
        product = get_object_or_404(ProductModel, uid=product_uid)

        quantity    =  validated_data.get('quantity', 1)

        validated_data['product_id'] = product 
        validated_data['price'] = product.price * quantity 
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """ """
        quantity = validated_data.get('quantity', instance.quantity)
        product  = instance.product_id 

        instance.quantity = quantity 
        instance.price = product.price * quantity
        instance.is_active = validated_data.get('is_active', instance.is_active)

        instance.save()
        return instance

class OrderModelSerializer(serializers.ModelSerializer):
    """
    Serializer for OrderModel.
    """
    class Meta:
        model = OrderModel
<<<<<<< HEAD
<<<<<<< HEAD
        fields = ['id', 'author', 'uid', 'order_num', 'status', , 'created', 'modified']
=======
        fields = ['id', 'author', 'uid', 'order_num', 'status',  'created', 'modified']
>>>>>>> dev
        read_only_fields = ('id', 'created', 'modified') 
=======
        fields = "__all__" # ['id', 'author','cart_id', 'uid', 'order_num',  'created', 'modified']
        read_only_fields = ('id','uid', 'order_num', 'created', 'modified') 
>>>>>>> dev


class OrderItemModelSerializer(serializers.ModelSerializer):
    """
    Serializer for OrderItemModel.
    """
    class Meta:
        model = OrderItemModel
        fields = ['id', 'uid', 'order_id', 'product_id', 'price', 'quantity', 'created', 'modified']
        read_only_fields = ('id', 'uid', 'price', 'created', 'modified')