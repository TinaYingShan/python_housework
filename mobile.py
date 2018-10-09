from urllib import parse,request
import html
import re
import json

def get_modile_region(mobile) :
    header_dict = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    }

    url = 'http://www.ip138.com:8080/search.asp?mobile=%s&action=mobile' % mobile
    req = request.Request(url=url, headers=header_dict)
    res = request.urlopen(req)
    ret = res.read()
    t = ret.decode('gbk').replace('&nbsp;', ' ').replace('\r\n', '')
    match = re.findall(r'<[Tt][Dd][^</>]*>卡号归属地</[Tt][Dd]>.*?<[Tt][Dd][^</>]+?>(<!-- <td></td> -->)?(?P<region>[^卡号归属地]+?)</[Tt][Dd]>', t)
    return match[0][1]

data = json.load(open('mobile_0.json','r',encoding='utf-8'))

for item in data['data']:
    region = get_modile_region(item['CELL_PHONE_NUMBER'])
    spilt = region.split(' ')
    item['province_mobile'] = spilt[0]
    item['city_mobile'] = spilt[0] if spilt[1] == '' else spilt[1]
    print(item)

json.dump(data, open('mobile_output.json','w',encoding='utf-8'))
# v = get_modile_region('1371206')
print(data)
