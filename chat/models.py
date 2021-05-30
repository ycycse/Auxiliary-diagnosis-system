import uuid

from django.db import models

from login.models import User


# Create your models here.


class ChatRoom(models.Model):
    """
    聊天室（供双人或多人）
    """
    name = models.CharField(max_length=255, null=True, verbose_name='聊天室名称')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False, editable=False)
    # name = models.CharField(max_length=128, verbose_name="群聊名称")
    members = models.ManyToManyField(User, verbose_name="聊天室成员")

    # 获取另一成员（仅针对双人聊天室）
    def get_another_member(self, member_name):
        members = self.members.all()
        if len(members) > 2:
            raise ValueError("members容量超出限制")

        another_member = members.exclude(username=member_name)[0]
        if not another_member:
            raise ValueError("members容量过小")
        return another_member

    # 获取聊天室内其他所有成员
    def get_other_members(self, member_name):
        members = self.members.all()

        other_members = members.exclude(username=member_name)
        if not other_members:
            raise ValueError("members容量过小")
        return other_members

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'chat_room'
        verbose_name_plural = verbose_name = '聊天室'


class Message(models.Model):
    """
    聊天信息模型
    """
    sender = models.ForeignKey(User, verbose_name="发送者", on_delete=models.CASCADE, related_name='sender_msg')
    chat_room = models.ForeignKey(ChatRoom, verbose_name="聊天室", on_delete=models.CASCADE, related_name='chatRoom_msg')
    text = models.CharField(max_length=255, verbose_name="信息内容")
    time = models.CharField(max_length=255, verbose_name="创建时间")
    READ = 'read'
    UNREAD = 'unread'
    STATUS_ITEM = (
        (READ, '已读'),
        (UNREAD, '未读'),
    )
    status = models.CharField(verbose_name="是否已读", choices=STATUS_ITEM, max_length=30, default=READ)
    receiver = models.ForeignKey(User, verbose_name="接收者", on_delete=models.CASCADE, related_name='receiver_msg')

    class Meta:
        db_table = "message"
        verbose_name_plural = verbose_name = "聊天信息"

    def __str__(self):
        return self.text

    @classmethod
    def get_receiver(cls, sender_name, chat_room):
        receiver = chat_room.get_another_member(sender_name)
        return receiver


class GroupMessage(models.Model):
    """
        群聊信息模型
    """
    sender = models.ForeignKey(User, verbose_name="发送者", on_delete=models.CASCADE, related_name="sender_g_msg")
    chat_room = models.ForeignKey(ChatRoom, verbose_name="聊天室", on_delete=models.CASCADE, related_name="chatRoom_g_msg")
    text = models.CharField(max_length=255, verbose_name="信息内容")
    time = models.CharField(max_length=255, verbose_name="创建时间")

    class Meta:
        db_table = "groupChat_message"
        verbose_name = verbose_name_plural = "群聊信息"

    def __str__(self):
        return self.text


class GroupMessageStatus(models.Model):
    """
        群聊信息状态模型
    """
    READ = 'read'
    UNREAD = 'unread'
    STATUS_ITEM = (
        (READ, '已读'),
        (UNREAD, '未读'),
    )
    status = models.CharField(verbose_name="是否已读", max_length=10, choices=STATUS_ITEM)
    message = models.ForeignKey(GroupMessage, on_delete=models.CASCADE, verbose_name="所属信息", related_name="gmsg_status")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="接收者", related_name="receiver_gmsgStatus")

    class Meta:
        db_table = 'group_msg_status'
        verbose_name = verbose_name_plural = "群聊信息状态"

    def __str__(self):
        return self.status
