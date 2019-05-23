# mysite/routing.py
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import OriginValidator
import connect.routing

"""
channels uses routing.py instead of django's urls.py
"""

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': OriginValidator ( 
        AuthMiddlewareStack(
            URLRouter(
                connect.routing.websocket_urlpatterns
            )
        ),
    [".localhost", ".herokuapp.com"] 
    )
})