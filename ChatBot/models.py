import uuid 
from django.db import models
from django.contrib.auth import get_user_model 

User = get_user_model() 

from core.timestamp import TimeStampModel

class ChatSession(TimeStampModel):
    author      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions')
    session_id  = models.UUIDField(default=uuid.uuid4, editable=False, unique=True) 
    title       = models.CharField(max_length=255, blank=True, null=True) 

    def __str__(self):
        return f"Chat Session {self.session_id} - {self.author.username}"
    
    class Meta:
        ordering = ['-created']   



class ChatMessage(TimeStampModel):

    ROLE_CHOICES =  (
        ('user', 'User'),
        ('assistant', 'Assistant'),
    )

    MESSAGE_TYPE_CHOICES = (
        ('text', 'Text'),
        ('code', 'Code'),
    )

    session         = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    role            = models.CharField(max_length=20, choices=ROLE_CHOICES)
    message_type    = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES, default='text')
    prompt          = models.TextField() 
    answer          = models.TextField(blank=True, null=True) 

    def __str__(self):
        return f"{self.role.capitalize()} - {self.session.session_id} - {self.created.strftime('%Y-%m-%d %H:%M:%S')}"

    class Meta:
        ordering = ['-created']
        
