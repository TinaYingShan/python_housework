#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
import urllib.request
import urllib.parse
import json
import re
import time
import smtplib
from email.message import EmailMessage
from email.headerregistry import Address
import threading


def get_weather_info(city_code):
    url = 'http://d1.weather.com.cn/dingzhi/%s.html?_=%d' % (
        city_code, time.time() * 1000)
    header = {
        'Referer': 'http://www.weather.com.cn/weather1d/%s.shtml' % city_code,
        'User-Agent': '''Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) 
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'''
    }
    request = urllib.request.Request(url=url, headers=header)
    response = urllib.request.urlopen(request).read().decode('utf-8')
    match = re.match(
        r'var cityDZ%s =(?P<weatherInfo>{[\s\S]*});var alarmDZ%s ={[\s\S]*}' % (city_code, city_code), response)
    return json.loads(match.group('weatherInfo'))['weatherinfo']


def get_weather(city_code):
    weather_info = get_weather_info(city_code)
    return weather_info['weather']


def send_notification(title, msg):
    message = EmailMessage()
    message['From'] = Address("YISH", addr_spec="mokeyish@yeah.net")
    message['To'] = Address("Tina", username='Tina.Yingshan', domain='hotmail.com')
    message['Cc'] = Address("YISH", addr_spec="mokeyish@yeah.net")
    message['Subject'] = title
    message.set_content(msg)
    message.set_charset('utf-8')

    try:
        smtp = smtplib.SMTP()
        smtp.connect("smtp.yeah.net", 25)  # 25 为 SMTP 端口号
        smtp.login("mokeyish@yeah.net", "z21954595")
        smtp.send_message(message)
        smtp.quit()
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("Error: 无法发送邮件")
        print(e)


last_weather = None


def check():
    print('检查天气')
    global last_weather
    global timer
    weather_info = get_weather_info('101210101')
    city = weather_info['cityname']
    weather: str = weather_info['weather']
    msg = '%s的天气: %s' % (city, weather)
    if weather != last_weather:
        print(msg)
        if weather.find('雨') > 0:
            if last_weather is None or last_weather.find('雨') == -1:
                send_notification('颖珊,下雨了记得带伞', msg)
        send_notification('颖珊天气有变=>%s' % msg, msg)
        last_weather = weather
    timer = threading.Timer(60, check)
    timer.start()


if __name__ == "__main__":
    timer = threading.Timer(1, check)
    timer.start()
