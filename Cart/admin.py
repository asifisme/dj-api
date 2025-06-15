from django.contrib import admin


from .models import CartModel 
from .models import CartItemModel
from .models import OrderModel
from .models import OrderItemModel 



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
    list_display = ( 'order_num', 'total_amount', 'author', 'ord_status', 'is_confirmed', 'created', 'modified',  )
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