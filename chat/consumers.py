"""定义consumer"""

"""第二版：同步调用channel_layer"""
import json
import time

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from login.models import User
from .models import Message
from .models import ChatRoom

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

        receiver = Message.get_receiver(sender_name=username, chat_room=chat_room)
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

        to_user = chat_room.get_another_member(username)
        print(to_user)
        for msg in messageList:
            msg_db = Message.objects.get(id=msg['id'])
            if msg_db.sender == to_user:
                msg_db.status = Message.READ
                msg_db.save()

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

        userList = total_room_userList.get(room_name)
        if not userList:
            total_room_userList[room_name] = []
            userList = total_room_userList.get(room_name)

        if username in userList:
            userList.remove(username)
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

        historyMessages = Message.objects.all()
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

    if code == 100:
        # 接收数据
        username = text_data_json.get('username')
        if not username:
            print("未接收到用户名数据")

        # 处理数据
        if username not in online_user_list:
            online_user_list.append(username)

        user = User.objects.get(username=username)
        unread_sender_list = []
        unread_message_list = Message.objects.filter(receiver=user).filter(status=Message.UNREAD)
        for unread_msg in unread_message_list:
            if unread_msg.sender.username not in unread_sender_list:
                unread_sender_list.append(unread_msg.sender.username)
                print(unread_sender_list)

        # 封装结果
        res = {
            'code': 100,
            'online_user_list': online_user_list,
            'newComer': username,
            'unread_sender_list': unread_sender_list,
        }

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

    if code == 200:
        sender_name = text_data_json.get('sender_name')
        text = text_data_json.get('text')
        room_id = text_data_json.get('room_id')

        try:
            chat_room = ChatRoom.objects.get(id=room_id)
        except:
            print("未找到相应聊天室")

        receiver = chat_room.get_another_member(sender_name)

        res = {
            'code': 200,
            'sender_name': sender_name,
            'text': text,
            'receiver_name': receiver.username,
            'room_id': room_id,
        }

    # 返回响应
    return res
