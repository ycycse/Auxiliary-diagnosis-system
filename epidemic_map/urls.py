"""为epidemic_map应用定义路由"""

from django.urls import path
from . import views

app_name = 'epidemic_map'
urlpatterns = [
    path('', views.ChinaMapView.as_view(), name='china-map'),
]
