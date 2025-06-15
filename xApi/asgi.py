

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter 
from django.core.asgi import get_asgi_application 
from channels.auth import AuthMiddlewareStack 
import Message 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xApi.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(Message.routing.websocket_urlpatterns)
    ),
})