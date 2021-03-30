"""为chat应用定义路由"""

from django.urls import path

from . import views

app_name = 'chat'
urlpatterns = [
    path('get_chat_room/<to_username>/', views.GetChatRoomView.as_view(), name='get_chat_room'),
    path('chat_room/<room_name>/', views.room, name='chat_room'),
    path('index/', views.IndexView.as_view(), name='chat_index'),
]
