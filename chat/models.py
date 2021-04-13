import uuid

from django.db import models

from login.models import User


# Create your models here.

 
class ChatRoom(models.Model):
    """
    聊天室（仅供双人）
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False, editable=False)
    # name = models.CharField(max_length=128, verbose_name="群聊名称")
    members = models.ManyToManyField(User, verbose_name="聊天室成员")

    def get_another_member(self, member_name):
        members = self.members.all()
        if len(members) > 2:
            raise ValueError("members容量超出限制")

        another_member = members.exclude(username=member_name)[0]
        if not another_member:
            raise ValueError("members容量过小")
        return another_member

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'chat_room'
        verbose_name_plural = verbose_name = '聊天室'


class Message(models.Model):
    """
    聊天信息模型
    """
    sender = models.ForeignKey(User, verbose_name="发送者", on_delete=models.CASCADE, related_name='sender')
    chat_room = models.ForeignKey(ChatRoom, verbose_name="聊天室", on_delete=models.CASCADE)
    text = models.CharField(max_length=255, verbose_name="信息内容")
    time = models.CharField(max_length=255, verbose_name="创建时间")
    READ = 'read'
    UNREAD = 'unread'
    STATUS_ITEM = (
        (READ, '已读'),
        (UNREAD, '未读'),
    )
    status = models.CharField(verbose_name="是否已读", choices=STATUS_ITEM, max_length=30, default=READ)
    receiver = models.ForeignKey(User, verbose_name="接收者", on_delete=models.CASCADE, related_name='receiver')

    class Meta:
        db_table = "message"
        verbose_name_plural = verbose_name = "聊天信息"

    def __str__(self):
        return self.text

    @classmethod
    def get_receiver(cls, sender_name, chat_room):
        receiver = chat_room.get_another_member(sender_name)
        return receiver
