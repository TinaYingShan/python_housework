from urllib import request
import  chardet, datetime


def get_weather_info(city_code, date):
    req = request.Request(
        url='http://tianqi.2345.com/t/wea_history/js/%s/%s_%s.js' % (date, city_code, date))
    res = request.urlopen(req)
    html = res.read()
    html = html.decode(chardet.detect(html)['encoding'], 'ignore')
    return html


startDate = datetime.datetime.strptime('2018-01-01', '%Y-%m-%d')
endDate = datetime.datetime.strptime('2018-09-30', '%Y-%m-%d')
currentDate = startDate
data = []
get_weather_info('58457', '58457')

print(data)

