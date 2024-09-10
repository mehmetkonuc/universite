import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from apps.notifications import routing as notifications_routing
from apps.chat import routing as chat_routing  # Chat routing'i ekliyoruz

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            notifications_routing.websocket_urlpatterns + chat_routing.websocket_urlpatterns  # İki routing'i birleştiriyoruz
        )
    ),
})
