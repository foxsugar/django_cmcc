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
from django.core import serializers
import zlib
from functools import wraps
import math
from testDjango.apps.models import *

COOKIES = {}
REDIS = redis.Redis(host='192.168.139.129', port=6379, db=0, password='123456')
MONTH_NUM = 6
PAGE_NUM = 200
conn = connect('test')
DETAIL_TYPE = {'fixed_exp': ['01', 'fixedExpList'],
               'call': ['02', 'callList'],
               'msg': ['03', 'messageList'],
               'net': ['04', 'netPlayList']
               }


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
    headers = {
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/Json',
        'Connection': 'Keep-Alive',
        'Content-Encoding': 'UTF-8',
        'Cookie2': '$Version=1'
    }
    postdata = bytes(json.dumps(data), 'utf8')

    request = urllib.request.Request(url, postdata, headers=headers, method='POST')
    cj = get_coodiejar(cell_num)
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    response = opener.open(request)

    return handle_response(cell_num, response)


def get_all_detail(cell_num):
    respondent_list = Respondents.objects.filter(cell_num=cell_num)
    if len(respondent_list) > 1:
        respondent = respondent_list[0]
    else:
        respondent = Respondents()

    for detail in DETAIL_TYPE:
        detail_type = DETAIL_TYPE[detail][0]
        list_month = get_in_recent_month(6)
        #测试用 只查一个月
        # list_month = ['2016-10']
        for month in list_month:
            rsp_str = get_detail_cmcc(cell_num, detail_type, month, 1, PAGE_NUM)
            print(rsp_str)
            rsp = json.loads(rsp_str)
            if rsp.get('retCode') == '000000' and rsp.get('rspBody') is not None:
                set_detail_by_response(respondent, month, detail, rsp_str)
                total_count = int(rsp.get('rspBody').get('totalCount'))
                page_size = math.ceil(total_count / (PAGE_NUM + 1))
                for i in range(2, page_size + 1):
                    rsp_str1 = get_detail_cmcc(cell_num, detail_type, month, i, PAGE_NUM)
                    print(rsp_str1)
                    set_detail_by_response(respondent, month, detail, rsp_str1)
                    time.sleep(2)

    """保存"""
    respondent.cell_num = cell_num
    respondent.save()


"""根据http返回储存"""
def set_detail_by_response(respondent, month, detail, rsp_str):
    detail_rsp_name = DETAIL_TYPE[detail][1]
    rsp = json.loads(rsp_str)
    d = getattr(respondent, detail)
    if rsp.get('rspBody') is not None and rsp.get('rspBody').get(detail_rsp_name) is not None:
        tmp_list = rsp.get('rspBody').get(detail_rsp_name)
        if d is not None:
            if d.get(month) is not None:
                d[month].extend(tmp_list)
            else:
                d[month] = [tmp_list]


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
    """获得cookiejar"""
    if COOKIES.get(cell_num) is None:
        cj = http.cookiejar.CookieJar()
        # data = serializers.serialize("json", cj)

        # print(type(data), data)
        # j = json.dumps(cj)
        # print(j)
        # REDIS.set(cell_num, json.dumps(cj))
        COOKIES[cell_num] = cj

    # print(eval(REDIS.get(cell_num)))
    # REDIS.get(cell_num)
    # print(eval(REDIS.get(cell_num)))
    # return json.loads(eval(REDIS.get(cell_num)))
    return COOKIES[cell_num]


def handle_response(cell_num, response):
    """处理response"""
    the_page = response.read()
    html = None
    if response is not None:
        # 是否压缩
        if response.headers.get('Content-Encoding') == 'gzip':
            # html = gzip.decompress(the_page).decode("utf-8")
            html = zlib.decompress(the_page, 16 + zlib.MAX_WBITS).decode("utf-8")
        else:
            html = the_page.decode('utf-8')
            # cookie
            # REDIS.set(cell_num, cj)

    return html


def create_headers(cell_num):
    """创建heraders"""
    headers = {'Accept-Encoding': 'gzip',
               'Content-Type': 'application/Json',
               'Connection': 'Keep-Alive',
               'Content-Encoding': 'UTF-8',
               }
    # handle_request_headers(cell_num, headers)
    return headers


# def handle_request_headers(cell_num, headers):
#     """添加cookie"""
#     if headers is not None:
#         if COOKIES.get(cell_num) is not None:
#             headers['Set-Cookie'] = COOKIES.get(cell_num)


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
        month_list.append(formart_month(now_year, now_month))
        if now_month <= 0:
            now_month = 12
            now_year -= 1
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
    # get_in_recent_month(6)

    d = {'a': []}

    d.get('a').extend([1, 2, 3])
    print(d)
