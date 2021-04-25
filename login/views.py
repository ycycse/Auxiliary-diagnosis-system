# import json
import re

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout, authenticate
from django.urls import reverse
from django.views import View
from django.http import HttpResponseForbidden, HttpResponse
from django.db import DatabaseError
# from .util import *
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator

from .models import User


# Create your views here.


# 登录
class LoginView(View):
    """用户登录"""

    def get(self, request):
        return render(request, 'login/login.html')

    @method_decorator(csrf_protect)
    def post(self, request):
        """登录逻辑"""
        # 接收参数
        # identity = request.POST.get('identity')

        username = request.POST.get('username')
        password = request.POST.get('password')

        # 校验参数
        if not all([username, password]):
            return HttpResponseForbidden("缺少必传参数")

        if not re.match(r'^[a-zA-Z0-9_\u4e00-\u9fa5\s·]+$', username):
            return HttpResponseForbidden("用户名不能有特殊字符")
        if not re.match(r'^[\S]{6,12}$', password):
            return HttpResponseForbidden("密码必须6到12位，且不能出现空格")

        # 从前端传来的identity参数是字符串，需转换
        # identity = int(identity)
        # 认证用户
        user = authenticate(username=username, password=password)
        if user is None:
            return render(request, 'login/login.html', {'login_errmsg': "账号或密码错误"})
        # else:
        #     if user.identity != identity:
        #         return render(request, 'login/login.html', {'login_errmsg': "身份不匹配"})

        # 状态保持
        login(request, user)

        next = request.GET.get('next')
        # 如果next存在则重定向至next
        if next:
            response = redirect(next)
        # 否则重定向至首页
        else:
            response = redirect(reverse('login:index'))

        # 设置cookie,将用户名保存至cookie当中
        response.set_cookie('username', username, max_age=3600 * 24 * 14)
        request.session['username'] = username
        request.session['nickname'] = user.nickname
        request.session['identity'] = user.identity

        # 响应结果:重定向至首页
        return response


# ajax验证
@csrf_protect
def verify_account(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    # identity = request.POST.get('identity')
    # identity = int(identity)
    print(username, password)
    # print(type(identity))
    response_data = {"info": 'false'}
    try:
        db_user = User.objects.get(username=username)
    except User.DoesNotExist as e:
        response_data = {"info": "username_false"}
        return JsonResponse(response_data, charset="utf-8")

    print(type(db_user.identity))
    if not db_user.check_password(password):
        print(db_user.password)
        response_data = {"info": "password_false"}
        return JsonResponse(response_data, charset="utf-8")
    # elif db_user.identity != identity:
    #     response_data = {'info': 'identity_false'}
    #     return JsonResponse(response_data, charset='utf-8')
    else:
        response_data = {"info": "true"}
        return JsonResponse(response_data, charset="utf-8")


# 退出方法
# @csrf_protect
def quit(request):
    # 清除状态保持信息
    logout(request)
    # 删除cookie中的username
    response = redirect(reverse('login:index'))
    response.delete_cookie('username')
    return response


# def page_not_found_error(request, exception):
#     return render(request, '404.html')
#
#
# def page_error(request):
#     return render(request, 'ztree.html')


# 首页模版
class IndexView(LoginRequiredMixin, View):
    """首页"""

    def get(self, request):
        # username = request.COOKIES.get('username')
        nickname = request.session.get('nickname')

        identity = request.session.get('identity')
        # identity需转化为整数类型
        identity = int(identity)
        # print(identity)

        if identity == User.DOCTOR:
            return render(request, 'index.html', {
                'nickname': nickname,
            })
        elif identity == User.PATIENT:
            # return render(request, 'index_patient.html', {
            #     'nickname': nickname,
            # })
            return render(request, 'index.html', {
                'nickname': nickname,
            })
        else:
            return HttpResponse("用户身份不合法")


class RegisterView(View):
    """注册视图"""

    def get(self, request):
        return render(request, 'login/register.html')

    @method_decorator(csrf_protect)
    def post(self, request):
        # 接收参数
        identity = request.POST.get('identity')

        username = request.POST.get('username')
        nickname = request.POST.get('nickname')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        print(identity, username, nickname, password2, password, phone, email)

        # 校验参数
        if not all([identity, username, nickname, password2, password, phone, email]):
            return HttpResponseForbidden('缺少必传参数')

        if not re.match(r'^[a-zA-Z0-9_\u4e00-\u9fa5\s·]+$', username):
            return HttpResponseForbidden("用户名不能有特殊字符")
        # if not re.match(r'',nickname):
        #     pass
        if not re.match(r'^[\S]{6,12}$', password):
            return HttpResponseForbidden("密码必须6到12位，且不能出现空格")
        if password2 != password:
            return HttpResponseForbidden("两次输入密码不一致")
        if not re.match(
                r'^[1](([3][0-9])|([4][5-9])|([5][0-3,5-9])|([6][5,6])|([7][0-8])|([8][0-9])|([9][1,8,9]))[0-9]{8}$',
                phone):
            return HttpResponseForbidden("请输入正确的手机号")
        if not re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
            return HttpResponseForbidden("请输入合法邮箱")

        # identity需转换
        identity = int(identity)

        # 保存用户数据
        try:
            user = User.objects.create_user(username=username, password=password, nickname=nickname, phone=phone,
                                            email=email, identity=identity)
        except DatabaseError:
            return render(request, 'login/register.html', {'register_errmsg': '注册失败'})

        # 实现状态保持（登录）
        login(request, user)

        response = redirect(reverse('login:index'))

        response.set_cookie('username', username, max_age=3600 * 24 * 14)
        request.session['nickname'] = nickname
        request.session['identity'] = identity
        request.session['username'] = username

        # 响应结果:重定向至首页
        return response


class UsernameCountView(View):
    """验证用户名是否重复注册"""

    @method_decorator(csrf_protect)
    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        return JsonResponse({"count": count})


class PhoneCountView(View):
    """验证手机号是否重复"""

    @method_decorator(csrf_protect)
    def get(self, request, phone):
        count = User.objects.filter(phone=phone).count()
        return JsonResponse({"count": count})
