"""
ASGI config for mapplebackend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "mapplebackend.settings"
)


from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

# ✅ VERY IMPORTANT: initialize Django FIRST
django_asgi_app = get_asgi_application()

# ⬇️ Only after this, import Django-dependent modules
import reviews.routing
import notifications.routing

from notifications.middleware import JWTAuthMiddleware



application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": JWTAuthMiddleware(
        URLRouter(
    reviews.routing.websocket_urlpatterns +
            notifications.routing.websocket_urlpatterns
)

    ),
})


