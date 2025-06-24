from django.urls import path, include 
from rest_framework.routers import DefaultRouter 

from .views import ChatSessionViewSet 
from .views import ChatBotViewSet 

router = DefaultRouter()

router.register(r'chat-session', ChatSessionViewSet, basename='chat-session')
router.register(r'chat', ChatBotViewSet, basename='chat-bot')

urlpatterns = [
    path('', include(router.urls)), 
]
