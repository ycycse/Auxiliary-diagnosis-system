from django.shortcuts import render
from django.views import View

# from .get_data import Get_data
# from . import execution
from .utils.get_data import Get_data


# Create your views here.


class ChinaMapView(View):
    """中国疫情地图"""

    def get(self, request):
        data = Get_data()
        data.get_data()
        time_in, time_out = data.get_time()
        data.parse_data()

        from .utils import execution

        execution.china_map(time_in)
        # execution.province_map(time_in)

        return render(request, 'map/中国疫情地图.html')
