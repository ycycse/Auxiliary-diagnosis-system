import json
import os

from copy import deepcopy

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.conf import settings

# from .get_data import Get_data
# from . import execution
from .utils.get_data import Get_data


# Create your views here.


class EpidemicMapView(View):
    """疫情可视化"""

    def get(self, request):
        return render(request, "map/epidemic_map.html")

    def post(self, request):

        # 读取现有轨迹数据
        track_path = os.path.join(settings.STATICFILES_DIRS[0], 'map', 'json', 'pandemic-tracks.json')
        if not os.path.exists(track_path) or not os.path.getsize(track_path):
            tracks = []
        else:
            with open(track_path, "r+", encoding='utf-8') as f:
                tracks = json.load(f)

        # 读取新用户数据
        nu_path = os.path.join(settings.STATICFILES_DIRS[0], 'map', 'json', 'new-users.json')
        if not os.path.exists(nu_path) or not os.path.getsize(nu_path):
            new_users = []
        else:
            with open(nu_path, "r+", encoding='utf-8') as nu_f:
                new_users = json.load(nu_f)

        # 获取用户名、经度、纬度数据
        name = request.session.get('username')
        coord_lng = float(request.POST.get('longitude'))
        coord_lat = float(request.POST.get('latitude'))
        coord = [coord_lng, coord_lat]

        in_track = False
        # 在现有轨迹中遍历
        for track in tracks:
            if track['name'] == name:
                track['coords'].append(coord)
                in_track = True
                break
        else:
            # 遍历新用户
            in_new_user = False
            for new_user in new_users:
                if new_user['name'] == name:
                    # 将其添加至现有轨迹中，并从新用户列表中删除
                    new_track = deepcopy(new_user)
                    new_users.remove(new_user)
                    new_track['coords'] = []
                    new_track['coords'].append(new_track['start_point'])
                    new_track['coords'].append(coord)
                    tracks.append(new_track)
                    in_new_user = True

        if not in_track and not in_new_user:
            new_users.append({
                "name": name,
                "start_point": coord,
            })

        if in_track or in_new_user:
            with open(track_path, "w", encoding='utf-8') as f:
                json.dump(tracks, f, indent=4, ensure_ascii=False)

        if not in_track:
            with open(nu_path, "w", encoding='utf-8') as f:
                json.dump(new_users, f, indent=4, ensure_ascii=False)

        return JsonResponse({
            'status': 'OK',
        })


class LocatinoUploadView(View):
    """位置上传视图"""

    def get(self, request):
        return render(request, "map/location_upload.html")
