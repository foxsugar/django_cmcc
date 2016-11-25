#!/usr/bin/python
# encoding=utf-8

import urllib.request
import time
import json


def main():
    submitUrl = 'http://op.juhe.cn/vercode/index'  # 接口地址
    appkey = '******'  # 接口申请的key
    codeType = '1005'  # 验证码的类型
    imagePath = 'D://test/1479437215.827385.jpg'  # 图片本地地址

    # buld post body data
    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    data.append('--%s' % boundary)

    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'key')
    data.append(appkey)
    data.append('--%s' % boundary)

    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'codeType')
    data.append(codeType)
    data.append('--%s' % boundary)

    fr = open(imagePath, 'rb')
    data.append('Content-Disposition: form-data; name="%s"; filename="b.png"' % 'image')
    data.append('Content-Type: %s\r\n' % 'image/png')
    data.append(fr.read())
    fr.close()
    data.append('--%s--\r\n' % boundary)

    print(data)
    http_body = '\r\n'.join(data)
    try:
        req = urllib.request.Request(submitUrl, data=http_body)

        # header
        req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
        req.add_header('User-Agent',
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36')
        req.add_header('Referer', 'http://op.juhe.cn/')

        resp = urllib.request.urlopen(req, timeout=30)

        qrcont = resp.read()

        result = json.loads(qrcont, 'utf-8')
        error_code = result['error_code']
        if (error_code == 0):
            data = result['result']  # 接口返回结果数据
            print(data)
        else:
            errorinfo = u"错误码:%s,描述:%s" % (result['error_code'], result['reason'])  # 返回不成功，错误码:原因
            print(errorinfo)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()