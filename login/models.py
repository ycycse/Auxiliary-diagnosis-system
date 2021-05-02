import uuid

# from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


# from mptt.models import MPTTModel


# Create your models here.


class User(AbstractUser):
    """自定义用户模型类"""

    DOCTOR = 0
    PATIENT = 1
    IDENTITY_ITEMS = (
        (DOCTOR, '医生'),
        (PATIENT, '患者'),
    )

    nickname = models.CharField(verbose_name="昵称", max_length=50, null=False)
    phone = models.CharField(verbose_name="电话", max_length=50, unique=True, null=False)
    identity = models.PositiveIntegerField(choices=IDENTITY_ITEMS, verbose_name='身份')

    class Meta:
        db_table = 'user'
        verbose_name_plural = verbose_name = "用户"

    def __str__(self):
        return self.nickname


class Patient(models.Model):
    ct_image = models.CharField(verbose_name="CT图片", max_length=128)
    ct_gt_image = models.CharField(verbose_name='分割图片', max_length=128)

    RET_ITEMS = (
        ('YES', '阳性'),
        ('NO', '阴性'),
    )
    examine_ret = models.CharField(verbose_name='检测结果', max_length=30, choices=RET_ITEMS)

    patient_to_user = models.OneToOneField(User, related_name='patient', on_delete=models.CASCADE)

    class Meta:
        db_table = 'patient'
        verbose_name_plural = verbose_name = '患者'
