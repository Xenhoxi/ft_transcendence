import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

# Set the default settings module for the Django application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transcendence.settings')

# Initialize the Django ASGI application
application = get_asgi_application()

# Import WebSocket routing patterns
from authentication.routing import websocket_urlpatterns as authentication_websocket_urlpatterns
from game.routing import websocket_urlpatterns as game_websocket_urlpatterns

# Combine all routing into a single application
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                authentication_websocket_urlpatterns + game_websocket_urlpatterns
            )
        )
    )
})

