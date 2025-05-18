from django.db import models
from django.contrib.auth import get_user_model 

from common.xtimestamp import TimeStampModel 

from xApiCart.models import OrderModel 


User = get_user_model() 


# class TimeStampModel(models.Model):
#     """
#     Abstract model to add created and modified timestamps
#     """
#     created      = models.DateTimeField(auto_now_add=True)
#     modified     = models.DateTimeField(auto_now=True)

#     class Meta:
#         abstract = True 


class PaymentModel(TimeStampModel):
    """
    Model to represent a payment 
    """
    order                  = models.OneToOneField(OrderModel, on_delete=models.CASCADE, related_name='payment') 
    user                   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments') 
    amount_paid            = models.IntegerField(null=True, blank=True)
    currency               = models.CharField(max_length=10, default="usd")
    stripe_checkout_id     = models.CharField(max_length=255, unique=True, null=True, blank=True) 
    stripe_payment_intent  = models.CharField(max_length=255, unique=True, null=True, blank=True)
    stripe_payment_status  = models.CharField(max_length=50, null=True, blank=True)
    stripe_payment_method  = models.CharField(max_length=255, null=True, blank=True) 
    receipt_url            = models.URLField(null=True, blank=True)


    def __str__(self)-> str:
        return f"Payment for Order {self.order.id} by {self.user.username}" 
    



