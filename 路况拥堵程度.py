import threading
import time
from urllib import request
import json
import socket
import postgresql

socket.setdefaulttimeout(5)


def get_clutter_road(longitude, latitude, key, radius):
    header_dict = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    }

    url = 'https://restapi.amap.com/v3/traffic/status/circle?location=%s,%s&key=%s&radius=%s' % (
        longitude, latitude, key, radius)

    req = request.Request(url=url, headers=header_dict)
    res = request.urlopen(req)
    ret = res.read()
    return json.loads(ret.decode('utf-8'))


# result = get_clutter_road(121.548104000000,30.040181000000, 'b22cf15d2011fc609e08ce25b772e1bf', 1000)


daily_task = {
    '%Y-%m-%d 07:00:00': None,
    '%Y-%m-%d 08:00:00': None,
    '%Y-%m-%d 09:00:00': None,
    '%Y-%m-%d 10:00:00': None,
    '%Y-%m-%d 11:00:00': None,
    '%Y-%m-%d 12:00:00': None,
    '%Y-%m-%d 13:00:00': None,
    '%Y-%m-%d 14:00:00': None,
    '%Y-%m-%d 15:00:00': None,
    '%Y-%m-%d 16:00:00': None,
    '%Y-%m-%d 17:00:00': None,
    '%Y-%m-%d 18:00:00': None,
    '%Y-%m-%d 19:00:00': None,
    '%Y-%m-%d 20:00:00': None,
    '%Y-%m-%d 21:00:00': None,
    '%Y-%m-%d 22:00:00': None,
    '%Y-%m-%d 00:00:00': None,
}


def collect_task():
    current_time = time.localtime()

    for i in daily_task:
        t = time.strftime(i, current_time)
        if daily_task[i] == t:
            continue

        t1 = time.strptime(t, '%Y-%m-%d %H:%M:%S')
        interval = (time.mktime(current_time) - time.mktime(t1)) / 60

        if 0 < interval < 5:
            db = postgresql.open('pq://root:123456@localhost:5432/ddqc')
            # 采集任务

            daily_task[i] = t
            return

    # print(get_clutter_road(121.548104000000, 30.040181000000, 'b22cf15d2011fc609e08ce25b772e1bf', 1000))


def do_work():
    global timer
    # noinspection PyBroadException
    try:
        collect_task()
    except:
        pass
    timer = threading.Timer(60, do_work)
    timer.start()


# db = postgresql.open('pq://root:123456@localhost:5432/ddqc')

#
# rows = db.prepare('select distinct "CELL_PHONE_NUMBER" from ddqc_data."TMP_STATE_CHARGING" where "CELL_PHONE_NUMBER" is not null and city_mobile is null')()
#
# for row in rows:
#     try:
#         phone = row[0]
#         region = get_mobile_region(phone)
#         spilt = region.split(' ')
#         province_mobile = spilt[0]
#         city_mobile = spilt[0] if spilt[1] == '' else spilt[1]
#         sql = "update ddqc_data.\"TMP_STATE_CHARGING\" set province_mobile='%s', city_mobile='%s' where \"CELL_PHONE_NUMBER\" ='%s'" % (province_mobile,city_mobile,phone)
#         db.execute(sql)
#         print(phone)
#     except Exception as e:
#         print(e)

# json.dump(data, open('mobile_output.json','w',encoding='utf-8'))
# v = get_modile_region('1371206')
# print(data)


if __name__ == "__main__":
    do_work()
