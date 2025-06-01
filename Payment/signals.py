
import controller 
import logging 
from decimal import Decimal
from django.db.models.signals import post_save 
from django.dispatch import receiver 
from django.core.mail import send_mail 
from django.conf import settings 

from .models import PaymentModel 
from Ledger.models import JournalEntryModel 

logger = logging.getLogger(__name__)


def create_journal_entry(instance): 
    try:
        order = instance.order 
        JournalEntryModel.objects.create(
                ent                  =order,
                ent_name             =order.order_items.first().product_id.name if order.order_items.exists() else 'Anon Products',
                ent_description      =f"Payment for Order #{order.order_num}",
                category             ='sales_revenue',
                status               ='posted',
                base_currency        =instance.currency.upper(),
                amount               =Decimal(instance.amount_paid) / 100,
                debit_amount         =Decimal(instance.amount_paid) / 100,
                credit_amount        =Decimal(instance.amount_paid) / 100,
                debit_name           ='bank_account',
                credit_name          ='sales_revenue',
                tax_amount           =Decimal('0.00'),
                author               =instance.user if hasattr(instance.user, "is_authenticated") and instance.user.is_authenticated else 1
            )
        logger.info(f"Journal entry created for payment: {instance.id}") 
    except Exception as e: 
        logger.error(f"Error creating journal entry for payment {instance.id}: {e}")




def send_payment_eamil(instance): 
    try:
        subject = f'Payment Confirmation for Order #{instance.order.id}'
        message = (

            f"Dear {instance.name_of_payer},\n\n"
            f"Thank you for your recent purchase with xApi.\n\n"
            f"We’re pleased to confirm that we have successfully received your payment of "
            f"${int(instance.amount_paid) // 100:.2f} {instance.currency.upper()} for your order #{instance.order.id}.\n\n"

            f"Here are your order details:\n"
            f"Order Number: {instance.order.order_num}\n"
            f"Amount Paid : ${int(instance.amount_paid) // 100:.2f} {instance.currency.upper()}\n"
            f"Payment Method: Stripe\n"
            f"Transaction ID: {instance.stripe_payment_intent or 'N/A'}\n"

            f"Your order is now being processed and will be dispatched shortly. "
            f"You will receive a shipping confirmation email once your items are on the way.\n\n"
            f"If you have any questions or need assistance, feel free to reply to this email "
            f"or contact our support team at {settings.DEFAULT_FROM_EMAIL}.\n\n"
            f"Thank you once again for choosing xApi. We truly appreciate your business.\n\n"
            f"Best regards,\n"
            f"The xApi Team\n"
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
        logger.error(f"Error sending payment confirmation email: {e}")




@receiver(post_save, sender=PaymentModel)
def handle_payment_post_save(sender, instance, created, **kwargs):
    """
    Signal for handling actions after payment creation.
    """
    if created:
        if controller.GLOBAL_EMAIL_SYSTEM and instance.stripe_checkout_id:
            # Send payment confirmation email
            send_payment_eamil(instance) 

        if controller.GLOBAL_JOURNAL_SYSTEM and instance.stripe_checkout_id:
            # Create journal entry
            create_journal_entry(instance) 

        logger.info(f"Payment processed for order: {instance.order.id}")