from django.db import models
from django.contrib.auth import get_user_model 

from core.timestamp import TimeStampModel 

from Cart.models import OrderModel 


User = get_user_model() 


class PaymentModel(TimeStampModel):
    """
    Model to represent a payment 
    """
    order                  = models.OneToOneField(OrderModel, on_delete=models.CASCADE, related_name='payment') 
    user                   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments') 
    name_of_payer          = models.CharField(max_length=255, null=True, blank=True)
    email_of_payer         = models.EmailField(null=True, blank=True)
    amount_paid            = models.IntegerField(null=True, blank=True)
    currency               = models.CharField(max_length=10, default="usd")
    stripe_checkout_id     = models.CharField(max_length=255, unique=True, null=True, blank=True) 
    stripe_payment_intent  = models.CharField(max_length=255, unique=True, null=True, blank=True)
    stripe_payment_status  = models.CharField(max_length=50, null=True, blank=True)
    stripe_payment_method  = models.CharField(max_length=255, null=True, blank=True) 
    receipt_url            = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ['-created'] 


    def __str__(self)-> str:
        return f"Payment for Order {self.order.id} by {self.user.username}" 
    




class PayPalPaymentModel(TimeStampModel):
    """
    Model to represent a PayPal payment
    """
    order                  = models.OneToOneField(OrderModel, on_delete=models.CASCADE, related_name='paypal_payment') 
    user                   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='paypal_payments') 
    name_of_payer          = models.CharField(max_length=255, null=True, blank=True)
    email_of_payer         = models.EmailField(null=True, blank=True)
    amount_paid            = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency               = models.CharField(max_length=10, default="usd")
    paypal_payment_id      = models.CharField(max_length=255, unique=True, null=True, blank=True) 
    paypal_payer_id        = models.CharField(max_length=255, null=True, blank=True) 
    paypal_token           = models.CharField(max_length=255, null=True, blank=True) 
    paypal_payment_status  = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ['-created'] 

    def __str__(self)-> str:
        return f"PayPal Payment for Order {self.order.id} by {self.user.username}"