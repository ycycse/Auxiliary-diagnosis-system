import json

from . import map_draw

map = map_draw.Draw_map()
# 格式
# map.to_map_china(['湖北'],['99999'],'1584201600')
# map.to_map_city(['荆门市'],['99999'],'湖北','1584201600')

# 获取数据
with open('data.json', 'r') as file:
    data = file.read()
    data = json.loads(data)


# 中国疫情地图
def china_map(update_time):
    area = []
    confirmed = []
    for each in data:
        # print(each)
        area.append(each['area'])
        confirmed.append(each['confirmed'])
    map.to_map_china(area, confirmed, update_time)


# 23个省、5个自治区、4个直辖市、2个特别行政区 香港、澳门和台湾的subList为空列表，未有详情数据

# 省、直辖市疫情地图
def province_map(update_time):
    for each in data:
        city = []
        confirmeds = []
        province = each['area']
        for each_city in each['subList']:
            city.append(each_city['city'] + "市")
            confirmeds.append(each_city['confirmed'])
            map.to_map_city(city, confirmeds, province, update_time)
        if province == '上海' or '北京' or '天津' or '重庆':
            for each_city in each['subList']:
                city.append(each_city['city'])
                confirmeds.append(each_city['confirmed'])
                map.to_map_city(city, confirmeds, province, update_time)
