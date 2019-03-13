import datetime
import urllib.parse
import urllib.request
import json


def get_week_day(date):
    week_day_dict = {
        0: '星期一',
        1: '星期二',
        2: '星期三',
        3: '星期四',
        4: '星期五',
        5: '星期六',
        6: '星期天',
    }
    day = date.weekday()
    return week_day_dict[day]


def get_holiday_info(date):
        url = 'http://api.goseek.cn/Tools/holiday?date=%s' % (
             datetime.datetime.strftime(date, "%Y%m%d"))
        request = urllib.request.Request(url=url)
        response = urllib.request.urlopen(request).read()
        return json.loads(response)['data']


def collect_data(start_date, end_date):
    i = start_date
    data = []
    while i < end_date :
        state = get_holiday_info(i)

        data.append({
            'date':datetime.datetime.strftime(i, "%Y%m%d"),'state':state,'week_day':get_week_day(i)
        })
        date = datetime.datetime.strftime(i, "%Y%m%d")
        print('%s %s' % (date, state))
        i = datetime.timedelta(days=1)+i

    return data


data = collect_data(datetime.datetime.strptime('2018-01-01', '%Y-%m-%d').date(), datetime.datetime.strptime('2018-01-20', '%Y-%m-%d').date())



with open('holiday.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(data, indent=2, ensure_ascii=False))
print('end')


