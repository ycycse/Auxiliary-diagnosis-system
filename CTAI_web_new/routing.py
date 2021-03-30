"""将根路由指向子应用的routing模块"""

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import chat.routing

# 当与channels开发服务器建立连接的时候，ProtocolTypeRouter将首先检查连接的类型。如果
# 是WebSocket连接，则连接会交给AuthMiddlewareStack.
application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    )
})
