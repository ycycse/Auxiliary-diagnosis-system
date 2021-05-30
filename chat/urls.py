"""为chat应用定义路由"""

from django.urls import path

from . import views

app_name = 'chat'
urlpatterns = [
    path('get_chat_room/<to_username>/', views.GetChatRoomView.as_view(), name='get_chat_room'),
    path('new_group_chat/', views.NewGroupChatView.as_view(), name='new_group_chat'),
    path('create_group_chat/', views.CreateGroupChatView.as_view(), name='create_group_chat'),
    path('get_group_chat/<room_name>/', views.GetGroupChatView.as_view(), name='get_group_chat'),
    path('chat_room/<room_name>/', views.room, name='chat_room'),
    path('index/', views.IndexView.as_view(), name='chat_index'),
]
