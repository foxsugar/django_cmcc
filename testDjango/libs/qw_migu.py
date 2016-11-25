# coding:utf-8

import urllib.request
import urllib.parse
import json
import gzip
import http.cookiejar
from bs4 import BeautifulSoup
import time
import datetime
import calendar
import redis

import zlib
from functools import wraps
import math


def main():
    url = 'http://www.55kaike.com/mobilesyn/EduOrder.aspx?paycode=300008025001'
    headers = {
        'Host':'www.55kaike.com',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Upgrade-Insecure-Requests':'1',
        'Connection':'keep-alive',
        'Accept-Encoding':'gzip, deflate',

    }

    request = urllib.request.Request(url,headers = headers, method='GET')

    response = urllib.request.urlopen(request)

    the_page = response.read()

    html = the_page.decode('utf-8')

    print(response)
    for i in response.headers:
        print(i + '  ' +response.headers[i])


    print(html)


def get_msg():
    pass


if __name__ == '__main__':
    main()