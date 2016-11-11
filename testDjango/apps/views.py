from django.shortcuts import render
import urllib
import httplib2
import http.client
from django.http import HttpResponse, Http404
import json
from django.template import loader
from django.shortcuts import render
from testDjango.libs.sendHttp import *
import time

def login(request):
    """A view of all bands."""
    cellNum = request.POST.get('name')
    passwd = request.POST.get('passwd')
    print(cellNum)
    print(passwd)

    respstr = login_cmcc(cellNum,passwd)
    resp = json.loads(respstr)
    print(respstr)

    #暂时放在该线程
    time.sleep(2)
    #获得验证码
    sendMsg_cmcc(cellNum)

    if resp.get('retCode') == '000000':
        return render(request, 'sendMsg.html', resp)
    else:
        return render(request, 'login.html', resp)
    # return HttpResponse(json.dumps(data), content_type="application/json")

    # return TemplateResponse(request, 'test.html', locals());
    # {"retCode": "110001", "retDesc": "系统繁忙,请稍后再试"}
    # {"retCode": "213000", "retDesc": "尊敬的用户，您好，您输入的手机号码和服务密码不匹配，请检查后重新输入"}
    # {"retCode": "000000", "retDesc": "SUCCESS",
    #  "rspBody": {"userName": "13821033039", "userBrand": "03", "userLevel": "", "userStatus": "00",
    #              "provinceCode": "220", "cityCode": "022", "provinceName": "天津", "cityName": "天津",
    #              "curTime": "2016-11-10 11:28:21"}}


def index(request):
    return render(request, 'login.html')




def verify_msg(request):
    """A view of all bands."""
    msg = request.POST.get('msg')
    cell_num = '13821033039'
    passwd = '102426'

    resp_str = verify_msg_cmcc(cell_num,passwd, msg)
    resp = json.loads(resp_str)
    print(resp)

    return render(request, 'getDetail.html', resp)
# {"retCode":"310002","retDesc":"字段名: passwd 长度非法! "}


def get_detail(request):
    cell_num = '13821033039'
    tmem_type = request.POST.get('type')
    month = request.POST.get('month')
    page = request.POST.get('page')
    unit = request.POST.get('unit')

    resp_str = get_detail_cmcc(cell_num, tmem_type, month, page, unit)
    print(resp_str)
    resp = json.loads(resp_str)
    print(resp)
    return render(request, 'main.html', resp)