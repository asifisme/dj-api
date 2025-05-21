import xcontroller 
import logging 
from django.db.models.signals import post_save 
from django.dispatch import receiver 
from django.core.mail import send_mail 
from django.conf import settings 


from .models import PaymentModel 
from xApiCart.models import OrderModel 


logger = logging.getLogger(__name__) 

if xcontroller.GLOBAL_EMAIL_SYSTEM:
    @receiver(post_save, sender=PaymentModel)
    def send_payment_confirmation_email(sender, instance, created, **kwargs):
        """
        Sends a payment confirmation email to the payer after successful payment.
        """
        if created:
            try:
                subject = f'Payment Confirmation for Order #{instance.order.id}'
                message = (
                    f'Dear {instance.name_of_payer},\n\n'
                    f'We have received your payment of {instance.amount_paid} {instance.currency}.\n'
                    f'Your order has been confirmed and is being processed.\n\n'
                    f'Thank you for shopping with us!\n\n'
                    f'- The Team'
                )

                recipient_email = [instance.email_of_payer]
                if recipient_email:
                    send_mail(
                        subject=subject,
                        message=message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=recipient_email,
                        fail_silently=False,
                    )
                    logger.info(f"Payment confirmation email sent to {instance.email_of_payer}.")
                else:
                    logger.warning(f"No recipient email provided for order {instance.order.id}.")

            except Exception as e:
                logger.exception(f"Error sending email for payment: {e}")
