import os
import time

from diagnosis.recognize import recognize
from diagnosis.segmentation import inference
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

# 返回在模板中的参数
context = {}


class PicProcessView(View):

    def getPicture(img_url):
        url = "models/segment/Results/Lung infection segmentation/Inf-Net/Append_result/%s" % img_url
        image_data = open(url, "rb").read()
        return HttpResponse(image_data, content_type="image/png")

    # 上传图片 分割后处理
    @csrf_exempt
    def post(self, request):

        print(request)
        file_url = ""

        file = request.FILES.get('file')  # 获取文件对象，包括文件名文件大小和文件内容
        curttime = time.strftime("%Y-%m-%d")
        # 规定上传目录
        upload_url = os.path.join(settings.MEDIA_ROOT, 'attachment', curttime)
        # 判断文件夹是否存在
        folder = os.path.exists(upload_url)
        if not folder:
            os.makedirs(upload_url)
            print("创建文件夹")
        if file:
            file_name = file.name
            # 判断文件是是否重名，懒得写随机函数，重名了，文件名加时间
            if os.path.exists(os.path.join(upload_url, file_name)):
                name, etx = os.path.splitext(file_name)
                addtime = time.strftime("%Y%m%d%H%M%S")
                finally_name = name + "_" + addtime + etx
            else:
                finally_name = file.name
            # 文件分块上传
            upload_file_to = open(os.path.join(upload_url, finally_name), 'wb+')
            for chunk in file.chunks():
                upload_file_to.write(chunk)
            upload_file_to.close()

            file_url = os.path.join(upload_url, finally_name)
            # 对类别进行识别
            context['judge'] = recognize(os.path.join(upload_url, finally_name))
            # 对图片进行分割
            context['append_img'] = inference(os.path.join(upload_url, finally_name))

            # 返回文件的URl
            file_upload_url = settings.MEDIA_URL + 'attachment/' + curttime + '/' + finally_name
            # 构建返回值
            response_data = {
                'code': 0,
                'msg': '',
                'data': {
                    'src': file_upload_url,
                }
            }
        else:
            print("no file")
        print(context)
        print("finished")
        return redirect("diagnosis:result_detail")


class PicUploadView(LoginRequiredMixin, View):
    """图片上传"""

    @method_decorator(xframe_options_sameorigin)
    def get(self, request):
        return render(request, 'diagnosis/pic_upload.html')


class MainLayoutView(View):
    @method_decorator(xframe_options_sameorigin)
    def get(self, request):
        return render(request, 'diagnosis/main_layout.html')


class ResultListView(View):
    @method_decorator(xframe_options_sameorigin)
    def get(self, request):
        return render(request, 'diagnosis/ct_resultList.html')


class ResultDetailView(View):
    @method_decorator(xframe_options_sameorigin)
    def get(self, request):
        return render(request, 'diagnosis/result_detail.html', context)


class ResultView(LoginRequiredMixin, View):
    """诊断结果显示"""
    pass
