import uuid 
from django.db import models, transaction
from django.contrib.auth import get_user_model
from decimal import Decimal 
from django.core.exceptions import ValidationError 
from django.core.validators import MinValueValidator


from Product.models import ProductModel 

from core.timestamp import TimeStampModel 




class TimeStampModel(models.Model):
    """
    Abstract base model that provides created and modified timestamps.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True 

User = get_user_model()




def cart_unique_key() -> str:
    """
    Generate a unique key for the cart. 
    """
    return uuid.uuid4().hex[:32].lower() 


class CartModel(TimeStampModel):
    """
    Model representing a shopping cart.
    """
    author          = models.OneToOneField(User,on_delete=models.CASCADE,related_name='carts')
    uid             = models.CharField(max_length=32, default=cart_unique_key,unique=True ) 

    class Meta:
        ordering = ['-created'] 

    def __str__(self) -> str:
        return f"Cart id : {self.id} {self.author.username}  "
    



def cart_item_unique_key() -> str:
    """
    Generate a unique key for the cart item.
    """
    return uuid.uuid4().hex[:32].lower() 


class CartItemModel(TimeStampModel):
    """
    Model representing an item in a shopping cart.
    """
    cart_id         = models.ForeignKey(CartModel, on_delete=models.CASCADE, related_name='cart_items')
    product_id      = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='cart_items')
    quantity        = models.PositiveIntegerField(default=1) 
    price           = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active       = models.BooleanField(default=True)
    uid             = models.CharField(max_length=32, default=cart_item_unique_key,unique=True)

    class Meta:
        ordering = ['-created']  

    def save(self, *args, **kwargs):
        if self.quantity == 0:
            if self.pk:
                self.delete()
            return
        super().save(*args, **kwargs) 
   
   
    def __str__(self) -> str:
        return f"Item {self.product_id.name} in Cart {self.cart_id.id}"
    
    
    



def order_unique_key() -> str:
    """
    Generate a unique key for the order.
    """
    return uuid.uuid4().hex[:32].lower() 


class OrderModel(TimeStampModel):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    PAYMENT_STATUS = (
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    )

    SHIPPING_STATUS = (
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('returned', 'Returned'),
        ('cancelled', 'Cancelled'),
    )


    author              = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    cart_id             = models.ForeignKey(CartModel, on_delete=models.CASCADE, related_name='orders')
    order_num           = models.BigIntegerField( unique=True, editable=False)
    order_note          = models.TextField(null=True, blank=True)
    ord_status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount        = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    payment_status      = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='unpaid')
    shipping_status     = models.CharField(max_length=20, choices=SHIPPING_STATUS, default='pending')
    is_confirmed        = models.BooleanField(default=False)
    uid                 = models.CharField(max_length=32, default=order_unique_key, unique=True)      

    class Meta:
        ordering = ['-created'] 


    def save(self, *args, **kwargs):
        """start order number from 1000000000"""
        if not self.order_num:
            last_order = OrderModel.objects.order_by('order_num').last()
            if last_order:
                self.order_num = last_order.order_num + 1
            else:
                self.order_num = 1000000000
    
        super().save(*args, **kwargs)


    def total_amount_calculation(self):
        total = 0
        for item in self.order_items.all():
            if item.product_id and item.product_id.price:
                total += Decimal(item.product_id.price) * Decimal(item.quantity) * (Decimal('1.0') - (Decimal(str(item.product_id.discount_percent)) / Decimal('100')))
        self.total_amount = total
        self.save()



    def __str__(self) -> str:
        """order number and first product name"""
        return f"{self.order_num}-{self.order_items.first().product_id.name if self.order_items.exists() else 'No Products'}" 
    



def order_item_unique_key() -> str:
    """
    Generate a unique key for the order item.
    """
    return uuid.uuid4().hex[:32].lower() 


class OrderItemModel(TimeStampModel):
    """
    Model representing an item in an order.
    """
    order_id            = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name='order_items')
    product_id          = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='order_items')
    quantity            = models.PositiveIntegerField(default=1)
    price               = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    uid                 = models.CharField(max_length=32, default=order_item_unique_key, unique=True) 

    class Meta:
        ordering = ['-created'] 

    def __str__(self) -> str:
        return f"Item {self.product_id.name} in Order {self.order_id.id}"



