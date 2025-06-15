from django.db import models
from django.contrib.auth import get_user_model 

from core.timestamp import TimeStampModel

User = get_user_model() 



class MessageModel(TimeStampModel):
    """
    Model to represent a message in the system.
    """

    class STATUS(models.TextChoices):
        DRAFT       = 'draft', 'Draft'
        DELIVERED   = 'delivered', 'Delivered' 
        SENT        = 'sent', 'Sent'
        RECEIVED    = 'received', 'Received'
        READ        = 'read', 'Read'

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS.choices, default=STATUS.DRAFT)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username}: {self.subject}"
    
    class Meta:
        ordering = ['-created'] 

