"""为diagnosis应用定义路由"""

from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'diagnosis'
urlpatterns = [
    path('pic_upload/', views.PicUploadView.as_view(), name='pic_upload'),
    path('pic_process/', views.PicProcessView.as_view(), name='pic_process'),
    path('result/', views.ResultView.as_view(), name='result'),
    path('main_layout/', views.MainLayoutView.as_view(), name='main_layout'),
    path('result_list/', views.ResultListView.as_view(), name='result_list'),
    path('result_detail/<num>/', views.ResultDetailView.as_view(), name='detail'),
    path('append_result/<img_url>/', views.PicProcessView.getPicture),
    path('update_result/<checked>/<result>/<idx>/', views.UpdateResultView.as_view())
]
