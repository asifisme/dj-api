from django.contrib import admin

from .models import PaymentModel 
from .models import PayPalPaymentModel 

@admin.register(PaymentModel)
class PaymentAdmin(admin.ModelAdmin):
    """
    Admin interface for PaymentModel
    """
    list_display = ('order', 'user', 'stripe_payment_status', 'created', 'modified') 
    search_fields = ('order__id', 'user__username', 'stripe_payment_status')
    list_filter = ('stripe_payment_status', 'created', 'modified')
    readonly_fields = ('created', 'modified')
    
    

@admin.register(PayPalPaymentModel)
class PayPalPaymentAdmin(admin.ModelAdmin):
    """
    Admin interface for PayPalPaymentModel
    """
    list_display = ('order', 'user', 'paypal_payment_status', 'created', 'modified') 
    search_fields = ('order__id', 'user__username', 'paypal_payment_status')
    list_filter = ('paypal_payment_status', 'created', 'modified')
    readonly_fields = ('created', 'modified') 