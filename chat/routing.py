"""配置通往consumer的路由，即配置websocket路由"""

from django.conf.urls import url
from django.urls import path

from . import consumers

websocket_urlpatterns = [
    # url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
    path('ws/chat/<room_name>/', consumers.ChatConsumer),
    path('wss/chat/<room_name>/', consumers.ChatConsumer),
    path('ws/group_chat/<room_name>/', consumers.GroupChatConsumer),
    path('wss/group_chat/<room_name>/', consumers.GroupChatConsumer),
]
