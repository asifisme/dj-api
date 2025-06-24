from django.contrib import admin

from .models import ChatSession 
from .models import ChatMessage 


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('author', 'session_id', 'title', 'created', 'modified')
    search_fields = ('author__username', 'session_id', 'title')


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('session', 'role', 'message_type', 'created')
    search_fields = ('session__session_id', 'role', 'message_type', 'prompt')
    list_filter = ('role', 'message_type')
    ordering = ('-created',)