import uuid 
from django.db import models, transaction
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from xApiProduct.models import ProductModel

User = get_user_model()


class TimeStampModel(models.Model):
    """
    Abstract model providing created and modified timestamps.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

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


    def __str__(self) -> str:
        return f"Cart id : {self.id} author email :  {self.author.email}"


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
    order_num           = models.BigIntegerField(default=1000000000, unique=True, editable=False)
    order_note          = models.TextField(null=True, blank=True)
    ord_status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount        = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    payment_status      = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='unpaid')
    shipping_status     = models.CharField(max_length=20, choices=SHIPPING_STATUS, default='pending')
    is_confirmed        = models.BooleanField(default=False)
    uid                 = models.CharField(max_length=32, default=order_unique_key, unique=True)      

    def save(self, *args, **kwargs):
        """start order number from 1000000000"""
        if not self.order_num:
            last_order = OrderModel.objects.order_by('order_num').last()
            if last_order:
                self.order_num = last_order.order_num + 1
            else:
                self.order_num = 1000000000
    
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Order {self.order_num} by {self.author.email} - Status: {self.ord_status}"


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



    def __str__(self) -> str:
        return f"Item {self.product_id.name} in Order {self.order_id.id}"
    



    # def clean(self) -> None:
    #     """
    #     Validate the order item before saving.
    #     """
    #     if self.quantity <= 0:
    #         raise ValidationError("Quantity must be greater than zero.")
    #     if not self.product_id.is_available():
    #         raise ValidationError(f"Product '{self.product_id.name}' is not available.")
    #     if not self.product_id.is_approved():
    #         raise ValidationError(f"Product '{self.product_id.name}' is not approved.")
    #     if self.product_id.stock is None or self.product_id.stock < self.quantity:
    #         raise ValidationError(f"Insufficient stock for product '{self.product_id.name}'.")

    # def save(self, *args, **kwargs) -> None:
    #     """
    #     Save the order item with validation and set price.
    #     """
    #     self.clean()
    #     with transaction.atomic():
    #         if not self.price and self.product_id.price:
    #             self.price = self.product_id.price
    #         self.product_id.reduce_stock(self.quantity)
    #         super().save(*args, **kwargs)