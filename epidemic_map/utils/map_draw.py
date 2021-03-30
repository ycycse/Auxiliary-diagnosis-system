from pyecharts import options as opts
from pyecharts.charts import Map
from django.conf import settings

import os


class Draw_map():
    # relativeTime为发布的时间,传入时间戳字符串
    # def get_time(self):
    # relativeTime = int(relativeTime)
    # return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(relativeTime))

    def __init__(self):
        if not os.path.exists(os.path.join(settings.BASE_DIR,'templates', 'map', 'china')):
            os.makedirs(os.path.join(settings.BASE_DIR,'templates', 'map', 'china'))

    def get_colour(self, a, b, c):
        result = '#' + ''.join(map((lambda x: "%02x" % x), (a, b, c)))
        return result.upper()

    '''
    参数说明——area：地级市 variate：对应的疫情数据 province：省份（不含省字）
    '''

    def to_map_city(self, area, variate, province, update_time):
        pieces = [
            {"max": 99999999, "min": 10000, "label": "≥10000", "color": self.get_colour(102, 2, 8)},
            {"max": 9999, "min": 1000, "label": "1000-9999", "color": self.get_colour(140, 13, 13)},
            {"max": 999, "min": 500, "label": "500-999", "color": self.get_colour(204, 41, 41)},
            {"max": 499, "min": 100, "label": "100-499", "color": self.get_colour(255, 123, 105)},
            {"max": 99, "min": 50, "label": "50-99", "color": self.get_colour(255, 170, 133)},
            {"max": 49, "min": 10, "label": "10-49", "color": self.get_colour(255, 202, 179)},
            {"max": 9, "min": 1, "label": "1-9", "color": self.get_colour(255, 228, 217)},
            {"max": 0, "min": 0, "label": "0", "color": self.get_colour(255, 255, 255)},
        ]

        c = (
            # 设置地图大小
            Map(init_opts=opts.InitOpts(width='1000px', height='880px'))
                .add("累计确诊人数", [list(z) for z in zip(area, variate)], province, is_map_symbol_show=False)
                # 设置全局变量  is_piecewise设置数据是否连续，split_number设置为分段数，pices可自定义数据分段
                # is_show设置是否显示图例
                .set_global_opts(
                title_opts=opts.TitleOpts(title="%s地区疫情地图分布" % (province),
                                          subtitle='截止%s  %s省疫情分布情况' % (update_time, province), pos_left="center",
                                          pos_top="10px"),
                legend_opts=opts.LegendOpts(is_show=False),
                visualmap_opts=opts.VisualMapOpts(max_=200, is_piecewise=True,
                                                  pieces=pieces,
                                                  ),
            )
                .render(
                os.path.join(settings.BASE_DIR, 'templates', 'map', 'china', '{}疫情地图.html'.format(province)))
        )

    def to_map_china(self, area, variate, update_time):
        pieces = [{"max": 999999, "min": 1001, "label": ">10000", "color": "#8A0808"},
                  {"max": 9999, "min": 1000, "label": "1000-9999", "color": "#B40404"},
                  {"max": 999, "min": 100, "label": "100-999", "color": "#DF0101"},
                  {"max": 99, "min": 10, "label": "10-99", "color": "#F78181"},
                  {"max": 9, "min": 1, "label": "1-9", "color": "#F5A9A9"},
                  {"max": 0, "min": 0, "label": "0", "color": "#FFFFFF"},
                  ]

        c = (
            # 设置地图大小
            Map(init_opts=opts.InitOpts(width='1000px', height='500px'))
                .add("累计确诊人数", [list(z) for z in zip(area, variate)], "china", is_map_symbol_show=False)
                .set_global_opts(
                title_opts=opts.TitleOpts(title="中国疫情地图分布", subtitle='截止%s 中国疫情分布情况' % (update_time), pos_left="center",
                                          pos_top="10px"),
                legend_opts=opts.LegendOpts(is_show=False),
                visualmap_opts=opts.VisualMapOpts(max_=200, is_piecewise=True,
                                                  pieces=pieces,
                                                  ),
            )
                .render(os.path.join(settings.BASE_DIR, 'templates', 'map', '中国疫情地图.html'))
        )
