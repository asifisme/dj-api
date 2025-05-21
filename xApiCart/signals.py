# signals.py
from django.db.models.signals import pre_save
from django.db.models.signals import post_save 
from django.db.models.signals import post_delete 
from django.dispatch import receiver
from .models import CartItemModel
from .models import OrderItemModel

@receiver(pre_save, sender=CartItemModel)
def update_cart_item_price(sender, instance, **kwargs):
    """Update price when quantity changes at DB level (e.g., via .update())."""
    if instance.product_id and instance.quantity:
        instance.price = instance.product_id.price * instance.quantity


@receiver([post_save, post_delete], sender=OrderItemModel)
def update_order_total(sender, instance, **kwargs):
    """Update the total amount of the order when an order item is saved or deleted."""
    instance.order_id.total_amount_calculation()