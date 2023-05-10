"""
ASGI config for geo_admin_suite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""


import os

import pathlib

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geo_admin_suite.settings')

asgi_application = get_asgi_application()

from apps.chat import routing
from apps.chat.middleware.channels_authentications import JwtAuthMiddleware

application = ProtocolTypeRouter({
    "http": asgi_application,
    "websocket": AllowedHostsOriginValidator(
        JwtAuthMiddleware(
            URLRouter(
                routing.websocket_urlpatterns,
            )
        )
    ),
})