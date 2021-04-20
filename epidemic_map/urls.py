"""为epidemic_map应用定义路由"""

from django.urls import path
from . import views

app_name = 'epidemic_map'
urlpatterns = [
    path('', views.EpidemicMapView.as_view(), name='epidemic-map'),
    path('location_upload/', views.LocatinoUploadView.as_view(), name='location-upload'),
]
