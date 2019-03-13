from urllib import request
import re
import socket
#import postgresql

socket.setdefaulttimeout(5) # 套接字(TCP/UDP...)，设置超时时间


def get_mobile_region(mobile) :
    header_dict = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    }

    url = 'http://www.ip138.com:8080/search.asp?mobile=%s&action=mobile' % mobile
    req = request.Request(url=url, headers=header_dict)  # request
    res = request.urlopen(req) # 获取响应 response
    ret = res.read() # 读取结果 reval 二进制数据
    t = ret.decode('gbk').replace('&nbsp;', ' ').replace('\r\n', '') # gbk 替换特殊html符号

    # 正则分组解析读取数据
    match = re.findall(r'<[Tt][Dd][^</>]*>卡号归属地</[Tt][Dd]>.*?<[Tt][Dd][^</>]+?>(<!-- <td></td> -->)?(?P<region>[^卡号归属地]+?)</[Tt][Dd]>', t)

    return match[0][1]


a = get_mobile_region('18602229647')

print("stop")
# data = json.load(open('mobile_0.json','r',encoding='utf-8'))
# total = data['data'].__len__()
# count = 0
# for item in data['data']:
#     try:
#         region = get_modile_region(item['CELL_PHONE_NUMBER'])
#         spilt = region.split(' ')
#         item['province_mobile'] = spilt[0]
#         item['city_mobile'] = spilt[0] if spilt[1] == '' else spilt[1]
#         count += 1
#         print(item)
#         print('完成:(%d/%d)'% (count, total))
#     except Exception as e:
#         print('获取归属地失败.')
#         print(e)


db = postgresql.open('pq://root:123456@localhost:5432/ddqc')


rows = db.prepare('select distinct "CELL_PHONE_NUMBER" from ddqc_data."TMP_STATE_CHARGING" where "CELL_PHONE_NUMBER" is not null and city_mobile is null')()

for row in rows:
    try:
        phone = row[0]
        region = get_mobile_region(phone)
        spilt = region.split(' ')
        province_mobile = spilt[0]
        city_mobile = spilt[0] if spilt[1] == '' else spilt[1]
        sql = "update ddqc_data.\"TMP_STATE_CHARGING\" set province_mobile='%s', city_mobile='%s' where \"CELL_PHONE_NUMBER\" ='%s'" % (province_mobile,city_mobile,phone)
        db.execute(sql)
        print(phone)
    except Exception as e:
        print(e)

# json.dump(data, open('mobile_output.json','w',encoding='utf-8'))
# v = get_modile_region('1371206')
# print(data)
print('complete!')
