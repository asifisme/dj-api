from rest_framework import serializers 

from .models import ChatSession 
from .models import ChatMessage 


class ChatSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model            = ChatSession
        fields           = ['id', 'author', 'session_id', 'title', 'created', 'modified']
        read_only_fields = ['id', 'author', 'session_id', 'title', 'created', 'modified'] 




class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model            = ChatMessage
        fields           = ['id', 'session', 'role', 'message_type', 'prompt', 'answer', 'created', 'modified']
        read_only_fields = ['id', 'session', 'role', 'answer', 'created', 'modified']
       
  