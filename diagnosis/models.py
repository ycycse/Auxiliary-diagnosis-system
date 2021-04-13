from django.db import models


# 用于储存检测结果 一次结果为一个元组
class DetectionResult(models.Model):
    # way:图片上传方式 为用户上传和医生上传
    # result:检测结果 为阴性与阳性
    # img_path:为上传图片的原图保存路径
    # processed_img_path:为分割处理后图片的保存路径
    # patient_id:患者的id号
    # index:结果序号
    # checked:是否被复查
    index = models.AutoField(primary_key=True)
    way = models.CharField(max_length=20)
    result = models.CharField(max_length=10)
    processed_img_path = models.CharField(max_length=100)
    img_path = models.CharField(max_length=100)
    patient_id = models.CharField(max_length=20)
    checked = models.BooleanField(default=False)

