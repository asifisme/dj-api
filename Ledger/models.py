import uuid
import datetime
from decimal import Decimal 
from django.db import models
from django.contrib.auth import get_user_model

from core.timestamp import TimeStampModel
from Cart.models import OrderModel


User = get_user_model()

def unique_voucher_number() -> str:
    """Generate a unique voucher number."""
    return uuid.uuid4().hex[:32].lower()

def tax_id_generator() -> str:
    """Generate a unique tax ID."""
    return uuid.uuid4().hex[:32].lower()



class JournalEntryModel(TimeStampModel, ):
    """
    Model to represent a journal entry for accounting purposes.
    """

    class CURRENCY(models.TextChoices):
        BDT = 'BDT', 'Bangladeshi Taka'
        USD = 'USD', 'United States Dollar'
        EUR = 'EUR', 'Euro'
        GBP = 'GBP', 'British Pound Sterling'

    class CATEGORY(models.TextChoices):
        # INCOME
        SALES_REVENUE       = 'sales_revenue', 'Sales Revenue'
        SERVICE_REVENUE     = 'service_revenue', 'Service Revenue'
        # EXPENSES 
        PURCHASES           = 'purchases', 'Purchases'
        RENT_EXPENSE        = 'rent_expense', 'Rent Expense'
        SALARY_PAYMENT      = 'salary_payment', 'Salary Payment' 
        UTILITY_BILLS       = 'utility_bills', 'Utility Bills' 


    class STATUS(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        POSTED = 'posted', 'Posted'
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
        COMPLETED = 'completed', 'Completed'

    # Transaction Details
    ent                    = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name='journal_entries', null=True, blank=True)
    ent_name               = models.CharField(max_length=255, null=True, blank=True)
    ent_description        = models.TextField(max_length=255, null=True, blank=True)
    ent_num                = models.DecimalField(max_digits=19, decimal_places=4, null=True, blank=True)

    # Category & Status
    category               = models.CharField(max_length=50, choices=CATEGORY.choices, default=CATEGORY.SALES_REVENUE)
    status                 = models.CharField(max_length=50, choices=STATUS.choices, default=STATUS.POSTED)

    # Currency & Tax
    base_currency           = models.CharField(max_length=10, choices=CURRENCY.choices, default=CURRENCY.USD)
    tax_amount              = models.DecimalField(max_digits=19, decimal_places=4, default=0.0)
    tax_id                  = models.CharField(max_length=255, default=tax_id_generator, unique=True)

    # Amounts
    amount                 = models.DecimalField(max_digits=19, decimal_places=4, default=0.0)
    debit_amount           = models.DecimalField(max_digits=19, decimal_places=4, default=0.0)
    credit_amount          = models.DecimalField(max_digits=19, decimal_places=4, default=0.0)

    # Account Names
    debit_name             = models.CharField(max_length=255, null=True, blank=True)
    credit_name            = models.CharField(max_length=255, null=True, blank=True)

    # Metadata
    reference_num          = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=True, blank=True) 
    ended                  = models.DateField(null=True, blank=True)
    # Author 
    author                 = models.ForeignKey(User, on_delete=models.PROTECT, related_name='journal_author', null=True, blank=True)


    class Meta:
        ordering = ['-created']


    def __str__(self):
        return f"{self.ent_name or 'Unnamed Entry'} - {self.ent_num or 'No Entry Num'}"

    def save(self, *args, **kwargs):
        if not self.ended:
            today = datetime.datetime.now().date()
            next_month = today.replace(day=1, month=(today.month % 12) + 1, year=today.year + (1 if today.month == 12 else 0))
            self.ended = next_month - datetime.timedelta(days=1)

        if not self.ent_num:
            last_entry = JournalEntryModel.objects.order_by('-ent_num').first()
            if last_entry and last_entry.ent_num:
                self.ent_num = last_entry.ent_num + Decimal('1.0000')
            else:
                self.ent_num = Decimal('10000.0000')

        super().save(*args, **kwargs)


