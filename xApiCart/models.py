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
    author          = models.OneToOneField(User,on_delete=models.CASCADE,related_name='carts',help_text="The user who owns this cart.")
    uid             = models.CharField(max_length=32, default=cart_unique_key, null=True, blank=True,
        help_text="Unique identifier for the cart."
    ) 


    def __str__(self) -> str:
        return f"Cart {self.id} by {self.author.username}"


def cart_item_unique_key() -> str:
    """
    Generate a unique key for the cart item.
    """
    return uuid.uuid4().hex[:32].lower() 

class CartItemModel(TimeStampModel):
    """
    Model representing an item in a shopping cart.
    """
    cart_id         = models.ForeignKey(CartModel, on_delete=models.CASCADE, related_name='cart_items', help_text="The cart this item belongs to.")
    product_id      = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='cart_items', help_text="The product in this cart item.")
    quantity        = models.PositiveIntegerField(default=1, help_text="The quantity of the product in the cart.")
    price           = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Snapshot price at time of adding to cart")
    is_active       = models.BooleanField(default=True, help_text="Indicates if the cart item is active.")
    uid             = models.CharField(max_length=32, default=cart_item_unique_key, null=True, blank=True)


    def __str__(self) -> str:
        return f"Item {self.product_id.name} in Cart {self.cart_id.id}"

    def clean(self) -> None:
        """
        Validate the cart item before saving.
        """
        if self.quantity <= 0:
            raise ValidationError("Quantity must be greater than zero.")
        if self.product_id.stock is None or self.product_id.stock < self.quantity:
            raise ValidationError(f"Insufficient stock for product '{self.product_id.name}'.")

    def save(self, *args, **kwargs) -> None:
        """
        Save the cart item with validation.
        """
        self.clean()
        super().save(*args, **kwargs)

        


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

    author              = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', help_text="The user who placed this order.")
    cart_id             = models.ForeignKey(CartModel, on_delete=models.CASCADE, related_name='orders', help_text="The cart associated with this order.")
    order_note          = models.TextField(null=True, blank=True, help_text="Optional notes for the order.")
    ord_status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', help_text="The status of the order.")
    total_amount        = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    payment_status      = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='unpaid')
    shipping_status     = models.CharField(max_length=20, choices=SHIPPING_STATUS, default='pending')
    is_confirmed        = models.BooleanField(default=False, help_text="Indicates if the order is confirmed.")
    uid                 = models.CharField(max_length=32, default=order_unique_key, null=True, blank=True)      

    
    def __str__(self) -> str:
        return f"Order {self.id} by {self.author.username}"
class Meta:
        indexes = [
            models.Index(fields=['author', 'ord_status']),
        ]


    # def save(self, *args, **kwargs) -> None:
    #     self.clean()
    #     with transaction.atomic():
    #         super().save(*args, **kwargs)
    #         if self.is_confirmed:
    #             for cart_item in self.cart_id.cart_items.all():
    #                 OrderItemModel.objects.create(
    #                     order_id=self,
    #                     product_id=cart_item.product_id,
    #                     quantity=cart_item.quantity,
    #                     price=cart_item.product_id.price
    #                 )
    #                 cart_item.product_id.reduce_stock(cart_item.quantity)
    #             self.cart_id.cart_items.update(is_active=False)

    # def confirm_order(self) -> None:
    #     if self.is_confirmed:
    #         raise ValidationError("Order is already confirmed.")
    #     with transaction.atomic():
    #         self.is_confirmed = True
    #         self.save()

    # def cancel_order(self) -> None:
    #     if self.ord_status == 'cancelled':
    #         raise ValidationError("Order is already cancelled.")
    #     with transaction.atomic():
    #         for item in self.order_items.all():
    #             item.product_id.stock += item.quantity
    #             item.product_id.save()
    #         self.ord_status = 'cancelled'
    #         self.save()


def order_item_unique_key() -> str:
    """
    Generate a unique key for the order item.
    """
    return uuid.uuid4().hex[:32].lower() 


class OrderItemModel(TimeStampModel):
    """
    Model representing an item in an order.
    """
    order_id            = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name='order_items', help_text="The order this item belongs to.")
    product_id          = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='order_items')
    quantity            = models.PositiveIntegerField(default=1, help_text="The quantity of the product in the order.")
    price               = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="The price of the product at the time of order.")
    uid                 = models.CharField(max_length=32, default=order_item_unique_key, null=True, blank=True) 

    class Meta:
        unique_together = ('order_id', 'product_id')
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"

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