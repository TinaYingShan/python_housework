#! /usr/local/bin/python3
import json
from urllib import request


def abc(month) :
    header_dict = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
        'Referer': 'http://www.weather.com.cn/weather40d/101210101.shtml'
    }

    url = 'http://d1.weather.com.cn/calendar_new/2018/101210101_2018'+month+'.html?_=1538495372953'
    req = request.Request(url=url, headers=header_dict)
    res = request.urlopen(req)
    ret = res.read()
    a = ret.decode('utf-8')[11:]
    jsonData = json.loads(a)
    return jsonData


data = []
for month in range(1, 10):
    monthData = abc('0'+str(month))
    data.extend(monthData)


with open('weather.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(data, indent=2, ensure_ascii=False))
print('end')
