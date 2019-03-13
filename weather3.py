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











if __name__ == "__main__":
    timer = threading.Timer(1, check)
    timer.start()
