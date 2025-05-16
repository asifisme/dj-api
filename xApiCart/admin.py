from django.contrib import admin

from xApiCart.models import CartModel 
from xApiCart.models import CartItemModel
from xApiCart.models import OrderModel
from xApiCart.models import OrderItemModel 


@admin.register(CartModel)
class CartModelAdmin(admin.ModelAdmin):
    """
    Admin interface for CartModel.
    """
    list_display = ('author', 'created', 'modified')
    search_fields = ('author__username',)
    list_filter = ('created', 'modified')
    ordering = ('-created',) 

@admin.register(CartItemModel)
class CartItemModelAdmin(admin.ModelAdmin):
    """
    Admin interface for CartItemModel.
    """
    list_display = ('cart_id', 'product_id', 'quantity', 'price', 'is_active')
    search_fields = ('cart_id__author__username', 'product_id__name')
    list_filter = ('is_active',)
    ordering = ('-created',) 

@admin.register(OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    """
    Admin interface for OrderModel.
    """
    list_display = ('id', 'author', 'cart_id', 'created', 'modified', 'ord_status', 'total_amount')
    search_fields = ('author__username',)
    list_filter = ('ord_status',)
    ordering = ('-created',) 


@admin.register(OrderItemModel)
class OrderItemModelAdmin(admin.ModelAdmin):
    """
    Admin interface for OrderItemModel.
    """
    list_display = ('id', 'order_id', 'product_id', 'quantity', 'price')
    search_fields = ('order_id__author__username', 'product_id__name')
    ordering = ('-created',) 