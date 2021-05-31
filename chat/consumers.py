"""定义consumer"""

"""第二版：同步调用channel_layer"""
import json
import time

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from login.models import User
from .models import Message, ChatRoom, GroupMessage, GroupMessageStatus

total_room_userList = {}
total_messageList = {}
online_user_list = []


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        if self.room_name == 'index':
            message = to_index_message(text_data_json)
        else:
            message = to_chat_message(text_data_json, self.room_group_name, self.room_name)

            # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',  # 指定consumer接收到event时调用的方法名称
                'message': message,
            }
        )

    # Send message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to Websocket
        self.send(text_data=json.dumps({
            'message': message,
        }))


# text_data_json:从前端接收到的json数据
# room_name: total_room_userList和total_messageList中的房间名
# room_id: 聊天室id
def to_chat_message(text_data_json, room_name, room_id):
    global total_room_userList
    global total_messageList
    global online_user_list
    code = text_data_json.get('code')
    chat_room = ChatRoom.objects.get(id=room_id)

    # 聊天信息
    if code == 200:
        # 接收数据
        username = text_data_json.get('username')
        text = text_data_json.get('text')

        # 处理数据
        user = User.objects.get(username=username)

        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        userList = total_room_userList.get(room_name)

        # 获取接收者
        receiver = Message.get_receiver(sender_name=username, chat_room=chat_room)
        # 判断接收者是否在聊天室中，若在则将创建信息状态置为已读，否则置为未读
        if len(userList) == 2:
            message = Message.objects.create(sender=user, chat_room=chat_room, text=text, time=now, status=Message.READ,
                                             receiver=receiver)
        elif len(userList) == 1:
            message = Message.objects.create(sender=user, chat_room=chat_room, text=text, time=now,
                                             status=Message.UNREAD, receiver=receiver)

        messageItem = {
            'id': message.id,
            'text': text,
            'sendUsername': username,
            'sendUserNickname': user.nickname,
            'time': now,
        }
        messageList = total_messageList.get(room_name)
        if not messageList:
            total_messageList[room_name] = []
            messageList = total_messageList.get(room_name)
        messageList.append(messageItem)
        total_messageList[room_name] = messageList

        # to_user = chat_room.get_another_member(username)
        # print(to_user)
        # for msg in messageList:
        #     msg_db = Message.objects.get(id=msg['id'])
        #     if msg_db.sender == to_user:
        #         msg_db.status = Message.READ
        #         msg_db.save()

        # 封装数据
        res = {
            'code': 200,
            'messageItem': messageItem,
            'messageList': messageList,
        }

    # 进入聊天室信息
    if code == 100:
        username = text_data_json.get('username')

        userList = total_room_userList.get(room_name)
        if not userList:
            total_room_userList[room_name] = []
            userList = total_room_userList.get(room_name)

        messageList = total_messageList.get(room_name)
        if not messageList:
            total_messageList[room_name] = []
            messageList = total_messageList.get(room_name)

        # 将当前加载在缓存中的对方发送的信息的状态置为已读
        to_user = chat_room.get_another_member(username)
        for msg in messageList:
            msg_db = Message.objects.get(id=msg['id'])
            if msg_db.sender == to_user:
                msg_db.status = Message.READ
                msg_db.save()

        if username not in userList:
            userList.append(username)
        total_room_userList[room_name] = userList

        res = {
            'code': 100,
            'userList': userList,
            'newComer': username,
            'messageList': messageList,
            'online_user_list': online_user_list,
        }

    # 离开聊天室信息
    if code == 888:
        username = text_data_json.get('username')

        # 获取该聊天室用户列表
        userList = total_room_userList.get(room_name)
        if not userList:
            total_room_userList[room_name] = []
            userList = total_room_userList.get(room_name)

        # 执行删除该用户操作
        if username in userList:
            userList.remove(username)
        # 更新本地total_room_userList
        total_room_userList[room_name] = userList

        res = {
            'code': 888,
            'userList': userList,
            'leave_user': username,
            'online_user_list': online_user_list,
        }

    # 请求历史数据
    if code == 666:
        # print(code)
        applicant = text_data_json.get('applicant')
        to_user = chat_room.get_another_member(applicant)

        # 获取当前聊天室历史数据
        historyMessages = Message.objects.filter(chat_room=chat_room)
        history_message_list = []
        for historyMessage in historyMessages:
            if historyMessage.sender == to_user:
                historyMessage.status = Message.READ
                historyMessage.save()

            history_message_item = {
                'text': historyMessage.text,
                'sendUsername': historyMessage.sender.username,
                'sendUserNickname': historyMessage.sender.nickname,
                'time': historyMessage.time,
            }
            history_message_list.append(history_message_item)

        res = {
            'code': 666,
            'history_message_list': history_message_list,
            'applicant': applicant,
        }

    # 返回数据
    return res


def to_index_message(text_data_json):
    global online_user_list
    code = text_data_json.get('code')

    # 用户上线
    if code == 100:
        # 接收数据
        username = text_data_json.get('username')
        if not username:
            print("未接收到用户名数据")

        # 处理数据
        if username not in online_user_list:
            online_user_list.append(username)

        # 获取当前用户
        user = User.objects.get(username=username)

        unread_sender_list = []
        # 基于双人聊天室信息记录查询有未读消息的发送者
        unread_message_list = Message.objects.filter(receiver=user).filter(status=Message.UNREAD)
        for unread_msg in unread_message_list:
            if unread_msg.sender.username not in unread_sender_list:
                unread_sender_list.append(unread_msg.sender.username)
                print(unread_sender_list)

        # 基于多人聊天室消息记录查询有未读消息的聊天室
        unread_g_chat_list = []

        # 获取当前用户所在的所有群聊
        chat_list = ChatRoom.objects.filter(members=user)
        g_chat_list = []  # 其中的是聊天室对象
        for chat_item in chat_list:
            if chat_item.members.count() > 2:
                g_chat_list.append(chat_item)

        # 获取群聊中所有信息记录(每个群聊对应一个消息列表)
        for g_chat in g_chat_list:
            # 获取该聊天室id
            g_chat_id = str(g_chat.id)
            # print(type(g_chat_id))
            # 获取该聊天室消息列表
            msg_list = GroupMessage.objects.filter(chat_room=g_chat)
            # 查询该聊天室中是否有对当前用户而言状态为未读的消息
            for msg in msg_list:
                msg_status = GroupMessageStatus.objects.filter(receiver=user, message=msg)
                if msg_status:
                    msg_status = msg_status[0].status
                    if msg_status == GroupMessageStatus.UNREAD:
                        unread_g_chat_list.append(g_chat_id)

        # 封装结果
        res = {
            'code': 100,
            'online_user_list': online_user_list,
            'newComer': username,
            'unread_sender_list': unread_sender_list,
            'unread_g_chat_list': unread_g_chat_list,
        }

    # 用户离线
    if code == 888:
        # 接收数据
        username = text_data_json.get('username')
        if not username:
            print("未接收到用户名数据")

        # 处理数据
        if username in online_user_list:
            online_user_list.remove(username)

        # 封装数据
        res = {
            'code': 888,
            'online_user_list': online_user_list,
            'leave_user': username,
        }

    # 用户发送消息
    if code == 200:
        sender_name = text_data_json.get('sender_name')
        text = text_data_json.get('text')
        room_id = text_data_json.get('room_id')

        try:
            chat_room = ChatRoom.objects.get(id=room_id)
        except:
            print("未找到相应聊天室")

        # 判断是双人聊天室还是多人聊天室
        members_count = chat_room.members.count()
        if members_count == 2:
            receiver = chat_room.get_another_member(sender_name)

            res = {
                'code': 200,
                'sender_name': sender_name,
                'text': text,
                'receiver_name': receiver.username,
                'room_id': room_id,
                'members_count': members_count,
            }
        else:
            res = {
                'code': 200,
                'sender_name': sender_name,
                'text': text,
                'room_id': room_id,
                'members_count': members_count,
            }

    # 返回响应
    return res


class GroupChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = to_group_chat_message(text_data_json, self.room_group_name, self.room_name)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',  # 指定consumer接收到event时调用的方法名称
                'message': message,
            }
        )

    def chat_message(self, event):
        message = event.get('message')

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
        }))


def to_group_chat_message(text_data_json, room_name, room_id):
    global total_room_userList
    global total_messageList

    # 获取信息种类码
    code = text_data_json.get('code')
    # 获取当前聊天室
    chat_room = ChatRoom.objects.get(id=room_id)

    # 用户发送聊天信息
    if code == 200:
        # 接收数据
        # 获取发送者用户名
        sender_name = text_data_json.get('username')
        # 获取文本信息
        text = text_data_json.get('text')

        # 处理数据
        # 查询得到sender
        sender = User.objects.get(username=sender_name)
        # 生成现在时间字符串
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        # 获取当前聊天室内的用户列表
        userList = total_room_userList.get(room_name)
        if not userList:
            total_room_userList[room_name] = []
            userList = total_room_userList.get(room_name)

        # 获取接收者列表
        receiverList = []
        for username in userList:
            if username == sender_name:
                continue
            else:
                receiverList.append(username)

        # 获取聊天室内其他所有成员
        other_members = chat_room.get_other_members(sender_name)

        # 创建消息对象
        g_message = GroupMessage.objects.create(sender=sender, chat_room=chat_room,
                                                text=text, time=now)
        # 对聊天室内的其他所有成员初始化该条信息的状态
        for other_member in other_members:
            g_msg_status = GroupMessageStatus.objects.create(message=g_message, receiver=other_member,
                                                             status=GroupMessageStatus.UNREAD)
            # 对当前聊天室内的所有接收者更新信息状态
            if other_member.username in receiverList:
                g_msg_status.status = GroupMessageStatus.READ
                g_msg_status.save()

        # 封装信息
        messageItem = {
            'id': g_message.id,
            'text': text,
            'sendUsername': sender_name,
            'sendUserNickname': sender.nickname,
            'time': now,
        }
        # 获取当前聊天室内的信息列表（缓存中
        messageList = total_messageList.get(room_name)
        if not messageList:
            total_messageList[room_name] = []
            messageList = total_messageList.get(room_name)
        # 更新缓存中信息列表
        messageList.append(messageItem)
        total_messageList[room_name] = messageList

        # 封装数据
        res = {
            'code': 200,
            'messageItem': messageItem,
            'messageList': messageList
        }

    # 进入聊天室信息
    if code == 100:
        # 接收进入聊天室用户的用户名
        username = text_data_json.get('username')

        # 获取当前用户
        user = User.objects.get(username=username)

        # 获取当前聊天室信息列表
        messageList = total_messageList.get(room_name)
        if not messageList:
            total_messageList[room_name] = []
            messageList = total_messageList.get(room_name)

        # 更新当前聊天室信息列表中的信息状态
        for messageItem in messageList:
            # 获取每条信息对应的数据库对象
            message_id = messageItem.get('id')
            g_message = GroupMessage.objects.get(id=message_id)
            # 对当前用户更新该条信息的状态
            g_msg_status = GroupMessageStatus.objects.filter(message=g_message, receiver=user)[0]
            print(g_msg_status)
            g_msg_status.status = GroupMessageStatus.READ
            g_msg_status.save()

        # 获取当前聊天室用户列表
        userList = total_room_userList.get(room_name)
        if not userList:
            total_room_userList[room_name] = []
            userList = total_room_userList.get(room_name)

        # 更新当前聊天室用户列表
        if username not in userList:
            userList.append(username)
        total_room_userList[room_name] = userList

        # 封装数据
        res = {
            'code': 100,
            'userList': userList,
            'newComer': username,
            'messageList': messageList,
            'online_user_list': online_user_list,
        }

    # 离开聊天室信息
    if code == 888:
        username = text_data_json.get('username')

        # 获取该聊天室用户列表
        userList = total_room_userList.get(room_name)
        if not userList:
            total_room_userList[room_name] = []
            userList = total_room_userList.get(room_name)

        # 执行删除该用户操作
        if username in userList:
            userList.remove(username)
        # 更新total_room_userList
        total_room_userList[room_name] = userList

        # 封装数据
        res = {
            'code': 888,
            'userList': userList,
            'leave_user': username,
            'online_user_list': online_user_list,
        }

    # 请求历史数据
    if code == 666:
        applicant_name = text_data_json.get('applicant')
        # 获取申请者用户
        applicant = User.objects.get(username=applicant_name)

        # 获取该聊天室历史信息
        history_g_msgs = GroupMessage.objects.filter(chat_room=chat_room)
        history_g_msg_list = []
        for history_g_msg in history_g_msgs:
            # 对申请者更新历史信息的状态
            history_g_msg_status = GroupMessageStatus.objects.filter(receiver=applicant, message=history_g_msg)[0]
            history_g_msg_status.status = GroupMessageStatus.READ
            history_g_msg_status.save()

            history_g_msg_item = {
                'text': history_g_msg.text,
                'sendUsername': history_g_msg.sender.username,
                'sendUserNickname': history_g_msg.sender.nickname,
                'time': history_g_msg.time,
            }
            history_g_msg_list.append(history_g_msg_item)

        # 封装数据
        res = {
            'code': 666,
            'history_g_msg_list': history_g_msg_list,
            'applicant': applicant_name,
        }

    # 返回数据
    return res
