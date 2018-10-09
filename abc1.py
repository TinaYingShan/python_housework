from urllib import parse, request
import  chardet, re, time, datetime

def getWeatherInfo(area, date):
    header_dict = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }
    form = {
        'txtdate': date,
        'txtareaName': area,
        '__VIEWSTATE': '/wEPDwUJNTIyODE2Mjk2D2QWAgIDEGRkFgICDQ8WAh4LXyFJdGVtQ291bnQCARYCAgEPZBYCZg8VCAbmna3lt54KMjAxOC0wOS0xNAblpJrkupEQ5Lic5YyX6aOOIDEtMue6pwUzMeKEgwblpJrkupEQ5Lic5YyX6aOOIDEtMue6pwUyNOKEg2RktwhuBc0ObMZ9obhG5ytq+jh2Xu4=',
        '__EVENTVALIDATION': '/wEWBAKikOGQCwKYt7mjAwLEhKj+DQKln/PuCk7JKQb+Ruw132Pe0SlZGj2Zpzr3'

    }
    data = parse.urlencode(form).encode('utf-8')
    req = request.Request(
        url='http://www.tianqihoubao.com/weather/city.aspx', headers=header_dict, data=data)
    res = request.urlopen(req)
    html = res.read()
    html = html.decode(chardet.detect(html)['encoding'], 'ignore')
    matches = re.findall(r'(?P<field><td>(?P<value>.*)<\/td>)', html)
    weatherInfo = {
        'area': area,  
        'date': matches[0][1],
        'day': matches[1][1],
        'dayWind': matches[2][1],
        'dayTemp': matches[3][1],
        'night': matches[4][1],
        'nightWind': matches[5][1],
        'nightemp': matches[6][1],
    }
    return weatherInfo
startDate = datetime.datetime.strptime('2018-01-01', '%Y-%m-%d')
endDate = datetime.datetime.strptime('2018-09-30', '%Y-%m-%d')
currentDate = startDate
data = []
while(currentDate < endDate):
    date = currentDate.strftime('%Y-%m-%d')
    data.append(getWeatherInfo('杭州', date))
    currentDate = currentDate + datetime.timedelta(days=1)

print(data)

