from django.urls import path, re_path
from .views import quit, verify_account  # , page_error, page_not_found_error
from . import views

app_name = 'login'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),  # 登录系统
    path('quit/', quit, name='quit'),  # 退出系统
    path('verify_account/', verify_account, name='verify_account'),  # 异步验证账号密码
    re_path(r'usernames/(?P<username>[a-zA-Z0-9_\u4e00-\u9fa5\s·]+)/count/$', views.UsernameCountView.as_view()),
    re_path(
        r'phones/(?P<phone>[1](([3][0-9])|([4][5-9])|([5][0-3,5-9])|([6][5,6])|([7][0-8])|([8][0-9])|([9][1,8,9]))[0-9]{8})/count/$',
        views.PhoneCountView.as_view()),
    path('', views.IndexView.as_view(), name='index'),
]
# handler404 = page_not_found_error
# handler500 = page_error
