import requests
from lxml import etree
import json
import re
import openpyxl


class Get_data():
    def get_data(self):
        # 目标url
        url = "https://voice.baidu.com/act/newpneumonia/newpneumonia/"

        # 伪装请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/80.0.3987.149 Safari/537.36 '
        }

        # 发出get请求
        response = requests.get(url,headers=headers)

        # 将请求的结果写入文件,便于分析
        with open('html.txt', 'w') as file:
            file.write(response.text)

    def get_time(self):
        with open('html.txt','r') as file:
            text = file.read()
        # 获取更新时间
        time_in = re.findall('"mapLastUpdatedTime":"(.*?)"',text)[0]
        time_out = re.findall('"foreignLastUpdatedTime":"(.*?)"',text)[0]
        # print('国内疫情更新时间为 '+time_in)
        # print('国外疫情更新时间为 '+time_out)
        return time_in,time_out

    def parse_data(self):
        with open('html.txt','r') as file:
            text = file.read()
        # 生成HTML对象
        html = etree.HTML(text)
        # 解析数据
        result = html.xpath('//script[@type="application/json"]/text()')
        # print(type(result))
        result = result[0]
        # print(type(result))
        result = json.loads(result)
        # print(type(result))
        result = json.dumps(result['component'][0]['caseList'])
        # print(result)
        # print(type(result))
        with open('data.json','w') as file:
            file.write(result)
            print('数据已写入json文件...')

        response = requests.get("https://voice.baidu.com/act/newpneumonia/newpneumonia/")
        # 将请求的结果写入文件,便于分析
        with open('html.txt', 'w') as file:
            file.write(response.text)

        # 获取时间
        time_in = re.findall('"mapLastUpdatedTime":"(.*?)"', response.text)[0]
        time_out = re.findall('"foreignLastUpdatedTime":"(.*?)"', response.text)[0]
        # print(time_in)
        # print(time_out)

        # 生成HTML对象
        html = etree.HTML(response.text)
        # 解析数据
        result = html.xpath('//script[@type="application/json"]/text()')
        # print(type(result))
        result = result[0]
        # print(type(result))
        result = json.loads(result)
        # print(type(result))
        # 以每个省的数据为一个字典
        data_in = result['component'][0]['caseList']
        # for each in data_in:
        #     print(each)
        #     print("\n" + '*' * 20)
        #
        data_out = result['component'][0]['globalList']
        # for each in data_out:
        #     print(each)
        #     print("\n" + '*' * 20)

        '''
        area --> 大多为省份
        city --> 城市
        confirmed --> 累计
        died --> 死亡
        crued --> 治愈
        relativeTime --> 
        confirmedRelative --> 累计的增量
        curedRelative --> 治愈的增量
        curConfirm --> 现有确诊
        curConfirmRelative --> 现有确诊的增量
        diedRelative --> 死亡的增量
        '''

        # 规律----遍历列表的每一项,可以发现,每一项(type:字典)均代表一个省份等区域,这个字典的前11项是该省份的疫情数据,
        # 当key = 'subList'时,其结果为只有一项的列表,提取出列表的第一项,得到一系列的字典,字典中包含该城市的疫情数据.

        # 将得到的数据写入excel文件
        # 创建一个工作簿
        wb = openpyxl.Workbook()
        # 创建工作表,每一个工作表代表一个area
        ws_in = wb.active
        ws_in.title = "国内疫情"
        ws_in.append(['省份', '累计确诊', '死亡', '治愈', '现有确诊', '累计确诊增量', '死亡增量', '治愈增量', '现有确诊增量'])
        for each in data_in:
            temp_list = [each['area'], each['confirmed'], each['died'], each['crued'], each['curConfirm'],
                         each['confirmedRelative'], each['diedRelative'], each['curedRelative'],
                         each['curConfirmRelative']]
            for i in range(len(temp_list)):
                if temp_list[i] == '':
                    temp_list[i] = '0'
            ws_in.append(temp_list)

        # 获取国外疫情数据
        for each in data_out:
            # print(each)
            # print("\n" + '*' * 20)
            sheet_title = each['area']
            # 创建一个新的工作表
            ws_out = wb.create_sheet(sheet_title)
            ws_out.append(['国家', '累计确诊', '死亡', '治愈', '现有确诊', '累计确诊增量'])
            for country in each['subList']:
                list_temp = [country['country'], country['confirmed'], country['died'], country['crued'],
                             country['curConfirm'], country['confirmedRelative']]
                for i in range(len(list_temp)):
                    if list_temp[i] == '':
                        list_temp[i] = '0'
                ws_out.append(list_temp)

            # 保存excel文件
            wb.save('./data.xlsx')
