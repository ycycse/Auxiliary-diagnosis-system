import json

from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views import View
from django.http import HttpResponseForbidden

from login.models import User
from .models import ChatRoom, Message


# Create your views here.


def room(request, room_name):
    """聊天室视图"""
    chat_room = ChatRoom.objects.get(id=room_name)
    username = request.session.get('username')
    from_user = User.objects.get(username=username)
    print(chat_room)

    current_to_user = chat_room.get_another_member(username)


    user_list = User.objects.all()
    # print(user_list)
    friend_list = []
    for user in user_list:
        if user.username == username:
            continue
        else:
            friend_item = {
                'username': user.username,
                'nickname': user.nickname,
                'identity': user.identity,
                # 'is_read': is_read,
            }
            friend_list.append(friend_item)

    chat_list = ChatRoom.objects.filter(members=from_user)
    to_user_list = []
    for chat in chat_list:
        to_user = chat.get_another_member(username)

        to_user_item = {
            'username': to_user.username,
            'nickname': to_user.nickname,
            'identity': to_user.identity,
            # 'is_read': is_read,
        }
        to_user_list.append(to_user_item)

    return render(request, 'chat/single-chat.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'current_to_user': current_to_user,
        'friend_list': friend_list,
        'to_user_list': to_user_list,
        # 'unread_sender_list': unread_sender_list,

    })


class IndexView(View):
    def get(self, request):
        # 获取数据
        username = request.session.get('username')
        if not username:
            print("登录状态有误，请重新登录")
            return HttpResponseForbidden("登录状态有误，请重新登录")

        # 处理数据

        user_list = User.objects.all()
        # print(user_list)
        friend_list = []
        for user in user_list:
            if user.username == username:
                continue
            else:

                friend_item = {
                    'username': user.username,
                    'nickname': user.nickname,
                    'identity': user.identity,
                    # 'is_read': is_read,
                }
                friend_list.append(friend_item)
        # print(friend_list)

        from_user = User.objects.get(username=username)
        chat_list = ChatRoom.objects.filter(members=from_user)
        to_user_list = []
        for chat in chat_list:
            to_user = chat.get_another_member(username)

            to_user_item = {
                'username': to_user.username,
                'nickname': to_user.nickname,
                'identity': to_user.identity,
                # 'is_read': is_read,
            }
            to_user_list.append(to_user_item)

        # 封装数据
        context = {
            'friend_list': friend_list,
            'to_user_list': to_user_list,
            # 'unread_sender_list': unread_sender_list,
        }

        # 返回响应
        return render(request, 'chat/index.html', context)


class GetChatRoomView(View):
    def get(self, request, to_username):
        print(to_username)
        # 接收数据
        from_username = request.session.get('username')
        from_user = User.objects.get(username=from_username)
        to_user = User.objects.get(username=to_username)
        print(to_user)

        # 处理数据
        chat_room = ChatRoom.objects.filter(members=from_user).filter(members=to_user).distinct()
        print(chat_room)
        if not chat_room:
            chat_room = ChatRoom.objects.create()
            chat_room.members.add(from_user, to_user)
        else:
            length = len(chat_room)
            if length > 1:
                return HttpResponseForbidden("存在多个聊天室")
            chat_room = chat_room[0]

        print(chat_room)
        print(chat_room.members.all())
        room_name = chat_room.id

        # 封装数据
        response = redirect(reverse('chat:chat_room', args=[room_name]))

        # 返回响应
        return response
