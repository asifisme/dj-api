from django.contrib import admin

from .models import PaymentModel 

@admin.register(PaymentModel)
class PaymentAdmin(admin.ModelAdmin):
    """
    Admin interface for PaymentModel
    """
    list_display = ('order', 'user', 'stripe_payment_status', 'created', 'modified') 
    search_fields = ('order__id', 'user__username', 'stripe_payment_status')
    list_filter = ('stripe_payment_status', 'created', 'modified')
    readonly_fields = ('created', 'modified')
    
    