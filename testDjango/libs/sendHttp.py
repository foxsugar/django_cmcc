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

COOKIES = {}
MONTH_NUM = 6


def login_cmcc(cell_num, passwd):
    url = 'https://clientaccess.10086.cn/biz-orange/LN/uamlogin/login'

    data = get_req_root()
    reqBody = {
        'cellNum': cell_num,
        'sendSmsFlag': '1',
        'ccPasswd': get_passwd(passwd)
    }

    data['reqBody'] = reqBody

    headers = {'Accept-Encoding': 'gzip',
               'Content-Type': 'application/Json',
               'Connection': 'Keep-Alive',
               'Content-Encoding': 'UTF-8'
               }

    postdata = bytes(json.dumps(data), 'utf8')
    request = urllib.request.Request(url, postdata, headers, method='POST')
    cj = get_coodiejar(cell_num)
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    response = opener.open(request)

    return handle_response(cell_num, response)


def sendMsg_cmcc(cell_num):
    url = 'https://clientaccess.10086.cn/biz-orange/LN/uamrandcode/sendMsgLogin'
    data = get_req_root()
    reqBody = {"cellNum": cell_num}
    data['reqBody'] = reqBody
    # postdata = urllib.parse.urlencode(data).encode('utf-8')
    postdata = bytes(json.dumps(data), 'utf8')

    headers = {'Accept-Encoding': 'gzip',
               'Content-Type': 'application/Json',
               'Connection': 'Keep-Alive',
               'Content-Encoding': 'UTF-8',
               }
    # handle_request_headers(cell_num, headers)

    request = urllib.request.Request(url, postdata, headers=headers, method='POST')
    cj = get_coodiejar(cell_num)
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    response = opener.open(request)
    return handle_response(cell_num, response)




def verify_msg_cmcc(cell_num, passwd, msg):
    url = 'https://clientaccess.10086.cn/biz-orange/LN/tempIdentCode/getTmpIdentCode'
    data = get_req_root()
    req_body = {
        'businessCode': '01',
        'cellNum': cell_num,
        'passwd': get_passwd(passwd),
        'smsPasswd': msg
    }
    data['reqBody'] = req_body
    headers = create_headers(cell_num)
    postdata = bytes(json.dumps(data), 'utf8')

    request = urllib.request.Request(url, postdata, headers=headers, method='POST')
    cj = get_coodiejar(cell_num)
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    response = opener.open(request)
    return handle_response(cell_num, response)


def get_detail_cmcc(cell_num, tmem_type, month, page, unit):
    url = 'https://clientaccess.10086.cn/biz-orange/BN/queryDetail/getDetail'
    data = get_req_root()
    req_body = {
        'billMonth': month,
        'cellNum': cell_num,
        'page': page,
        'tmemType': tmem_type,
        'unit': unit
    }
    data['reqBody'] = req_body
    postdata = bytes(json.dumps(data), 'utf8')
    headers = create_headers(cell_num)
    headers['Cookie2'] = '$Version=1'

    request = urllib.request.Request(url, postdata, headers=headers, method='POST')
    cj = get_coodiejar(cell_num)
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    response = opener.open(request)

    return handle_response(cell_num, response)


def get_all_detail(cell_num):
    t = time.time()


def get_cid():
    url = 'http://localhost:5000/?type=cid'
    response = urllib.request.urlopen(url)
    the_page = response.read()
    # soup = BeautifulSoup(the_page, "html.parser", from_encoding="utf-8")
    return the_page.decode('utf-8')


def get_passwd(passwd):
    url = 'http://localhost:5000/?type=pwd&param=' + passwd
    response = urllib.request.urlopen(url)
    the_page = response.read()

    return the_page.decode('utf-8')


def get_coodiejar(cell_num):
    if COOKIES.get(cell_num) is None:
        cj = http.cookiejar.CookieJar()
        COOKIES[cell_num] = cj
    return COOKIES.get(cell_num)


def handle_response(cell_num, response):
    """处理response"""
    the_page = response.read()
    html = None
    if response is not None:
        # 是否压缩
        if response.headers.get('Content-Encoding') == 'gzip':
            html = gzip.decompress(the_page).decode("utf-8")
        else:
            html = the_page.decode('utf-8')

    return html


def create_headers(cell_num):
    headers = {'Accept-Encoding': 'gzip',
               'Content-Type': 'application/Json',
               'Connection': 'Keep-Alive',
               'Content-Encoding': 'UTF-8',
               }
    # handle_request_headers(cell_num, headers)
    return headers


def handle_request_headers(cell_num, headers):
    """添加cookie"""
    if headers is not None:
        if COOKIES.get(cell_num) is not None:
            headers['Set-Cookie'] = COOKIES.get(cell_num)


def get_req_root():
    data = {'cid': get_cid(),
            'cv': '2.3.0',
            'en': '0',
            'sn': 'EVA-TL00',
            'sp': '1080x1812',
            'st': '1',
            'sv': '6.0',
            't': ''
            }
    return data


def get_in_recent_month(num):
    """获得最近的num个月字符串"""
    month_list = []
    now = datetime.datetime.now()
    now_year = int(now.strftime('%Y'))
    now_month = int(now.strftime('%m'))

    for i in range(0, num):
        if now_month <= 0:
            now_month = 12
            now_year -= 1
            month_list.append(formart_month(now_year, now_month))
        now_month -= 1
    return month_list


def formart_month(year, month):
    """拼接月份"""
    if month < 10:
        return ''.join([str(year), '-', '0', str(month)])
    else:
        return ''.join([str(year), '-', str(month)])


if __name__ == '__main__':
    # login_cmcc('13821033039', '102426')
    # print(time.time())
    # print(time.localtime())
    # print(datetime.datetime.now())
    # now = datetime.datetime.now()
    # print(now.strftime('%Y-%m'))
    # print(now.microsecond)
    #
    # time_temp = '201504'
    # # dt = datetime.date(int(time_temp[0:4]), int(time_temp[4:6]), int(time_temp[6:8]))
    # # print(months(dt,-1))
    # print(int('04'))
    # now = datetime.datetime.now()
    # int(now.strftime('%Y'))
    get_in_recent_month(6)
