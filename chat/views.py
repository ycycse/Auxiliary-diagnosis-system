import json

from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views import View
from django.http import HttpResponseForbidden, HttpResponse, JsonResponse

from login.models import User
from .models import ChatRoom, Message


# Create your views here.

def get_sidebar_infos(username, from_user):
    # 获取好友列表
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

    # 得到聊天室列表（包括双人和多人）
    chat_list = ChatRoom.objects.filter(members=from_user)
    # 最近聊天列表
    to_user_list = []
    # 多人聊天室列表
    g_chat_list = []
    for chat in chat_list:
        members = chat.members.all()
        if len(members) == 2:
            to_user = chat.get_another_member(username)

            to_user_item = {
                'username': to_user.username,
                'nickname': to_user.nickname,
                'identity': to_user.identity,
                # 'is_read': is_read,
            }
            to_user_list.append(to_user_item)
        elif len(members) > 2:
            g_chat_item = {
                'g_chat_id': chat.id,
                'g_chat_name': chat.name,
            }

            g_chat_list.append(g_chat_item)

    return friend_list, to_user_list, g_chat_list


def room(request, room_name):
    """聊天室视图"""
    chat_room = ChatRoom.objects.get(id=room_name)
    username = request.session.get('username')
    from_user = User.objects.get(username=username)
    print(chat_room)

    # 获取侧边栏数据
    friend_list, to_user_list, g_chat_list = get_sidebar_infos(username, from_user)

    current_to_user = chat_room.get_another_member(username)

    return render(request, 'chat/single-chat.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'current_to_user': current_to_user,
        'friend_list': friend_list,
        'to_user_list': to_user_list,
        'g_chat_list': g_chat_list,
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
        from_user = User.objects.get(username=username)

        # 获取侧边栏数据
        friend_list, to_user_list, g_chat_list = get_sidebar_infos(username, from_user)

        # 封装数据
        context = {
            'friend_list': friend_list,
            'to_user_list': to_user_list,
            'self': from_user,
            'g_chat_list': g_chat_list,
            # 'unread_sender_list': unread_sender_list,
        }

        # 返回响应
        return render(request, 'chat/index.html', context)


class GetChatRoomView(View):
    """
        获取或创建双人聊天室
    """

    def get(self, request, to_username):
        print(to_username)
        # 接收数据
        from_username = request.session.get('username')
        from_user = User.objects.get(username=from_username)
        to_user = User.objects.get(username=to_username)
        print(to_user)

        # 处理数据
        # 获取聊天室列表
        chat_room_list = ChatRoom.objects.filter(members=from_user).filter(members=to_user).distinct()
        # 筛选得到双人聊天室列表
        single_room_list = []
        for chat_room_item in chat_room_list:
            if chat_room_item.members.count() == 2:
                single_room_list.append(chat_room_item)

        print(single_room_list)
        if not single_room_list:
            single_room = ChatRoom.objects.create()
            single_room.members.add(from_user, to_user)
        else:
            length = len(single_room_list)
            if length > 1:
                return HttpResponseForbidden("存在多个聊天室")
            single_room = single_room_list[0]

        print(single_room)
        print(single_room.members.all())
        room_name = single_room.id

        # 封装数据
        response = redirect(reverse('chat:chat_room', args=[room_name]))

        # 返回响应
        return response


class CreateGroupChatView(View):
    """
    新建群聊
    """

    def post(self, request):
        # 接收数据
        # print(request.POST)
        members = request.POST.get('members')
        members = json.loads(members)
        group_chat_name = request.POST.get('group_chat_name')
        # print(group_chat_name)

        # 创建群聊
        chat_room = ChatRoom.objects.create(name=group_chat_name)
        # 添加成员
        for username in members:
            user = User.objects.get(username=username)
            chat_room.members.add(user)
        self_name = request.session.get('username')
        self_user = User.objects.get(username=self_name)
        chat_room.members.add(self_user)

        print(chat_room)
        print(chat_room.members.all())

        # 下一步需要给多人聊天室创建单独的视图函数和前端页面

        return JsonResponse({
            'status': 'OK',
        })


class NewGroupChatView(View):
    """
    返回新建群聊表单页面
    """

    def get(self, request):
        return render(request, 'chat/view/createGroupChat.html')

    def post(self, request):
        # 从session中获取相应参数
        username = request.session.get('username')
        if not username:
            print("登录状态有误，请重新登录")
            return HttpResponseForbidden("登录状态有误，请重新登录")

        # print(username)
        # 处理参数
        user_list = User.objects.all()
        # print(user_list)
        friend_list = []
        index = 1
        for user in user_list:
            if user.username == username:
                continue
            else:
                friend_item = {
                    'value': index,
                    'title': user.nickname + '(' + user.username + ')',
                    'disabled': '',
                    'checked': '',
                }
                index = index + 1
                friend_list.append(friend_item)
        # print(friend_list)

        return JsonResponse({
            'status': 'OK',
            'friend_list': friend_list,
        })


class GetGroupChatView(View):
    """
        获取多人聊天室视图
    """

    def get(self, request, room_name):
        """

        :param request:
        :param room_name: 多人聊天室id
        :return:
        """
        print(room_name)

        # 获取聊天室对象
        chat_room = ChatRoom.objects.get(id=room_name)
        g_chat_name = chat_room.name
        members_count = chat_room.members.count()
        # 获取用户名
        username = request.session.get('username')
        if not username:
            return HttpResponseForbidden("您的登录状态有误，请重新登录")
        # 获取用户对象
        from_user = User.objects.get(username=username)

        # 获取侧边栏数据
        friend_list, to_user_list, g_chat_list = get_sidebar_infos(username, from_user)

        # 封装数据
        context = {
            'room_name_json': mark_safe(json.dumps(room_name)),
            # 'current_to_user': current_to_user,
            'friend_list': friend_list,
            'to_user_list': to_user_list,
            'g_chat_list': g_chat_list,
            'g_chat_name': g_chat_name,  # 聊天室名称
            'members_count': members_count,  # 成员数量
        }

        # 返回响应
        return render(request, 'chat/group-chat.html', context)
