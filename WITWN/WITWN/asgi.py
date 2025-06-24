"""
ASGI config for WITWN project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import chat_app.routing as chat_route
import core_app.routing as core_route
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WITWN.settings')

application = ProtocolTypeRouter({ 
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(core_route.ws_urlpatterns + chat_route.ws_urlpatterns)
    )
})