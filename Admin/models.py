from django.db import models
from django.contrib.auth import get_user_model
from core.timestamp import TimeStampModel 

User    = get_user_model()

class MailTable(TimeStampModel):

    class MailStatus(models.TextChoices):
        DRAFT       = 'draft', 'Draft'
        PENDING     = 'pending', 'Pending'
        SENT        = 'sent', 'Sent'
        FAILED      = 'failed', 'Failed'

    author      = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    subject     = models.CharField(max_length=255, blank=True)
    message     = models.TextField(blank=True)
    to_email    = models.EmailField(max_length=255, blank=True)
    status      = models.CharField(max_length=255, choices=MailStatus.choices, default='draft')

    def __str__(self):
        return f'{self.author}-{self.subject}'