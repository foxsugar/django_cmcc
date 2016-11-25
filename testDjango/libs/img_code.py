# coding:utf-8
import urllib.request
import urllib.parse
import hashlib
from struct import *
import zlib
import time

def get_code():
    url = 'https://passport.migu.cn/captcha/graph?imgcodeType=1&t=0.48289718264740245'
    # url = 'http://wap.dm.10086.cn/capability/capacc/imgCode?session=1702020263&randnum=638120'



    headers = {
                'Accept-Encoding': 'gzip, deflate, sdch, br',
               # 'Content-Type': 'application/Json',
                'Accept-Language': 'zh-CN,zh;q=0.8',
               'Connection': 'Keep-Alive',
               'Content-Encoding': 'UTF-8',
               'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
               'Upgrade-Insecure-Requests':'1',

               }

    request = urllib.request.Request(url, headers=headers, method='GET')
    response = urllib.request.urlopen(request)
    the_page = response.read()

    print(type(the_page))
    print(the_page)
    md5 = get_md5(the_page)

    # result = urllib.request.urlretrieve(url, save('d://test/'+md5+'.jpg'))
    save_file('d://test1/'+md5+'.jpg',the_page)
    # save('d://test/'+md5+'.jpg')
    # print(result)

def get_img():
    while(True):
        try:
            # url = 'https://passport.migu.cn/captcha/graph?imgcodeType=1&t=0.48289718264740245'
            url = 'http://wap.dm.10086.cn/capability/capacc/imgCode?session=1702020263&randnum=638120'
            t = time.time()
            filename = save('d://test_cmcc/' + str(t)+ '.jpg')
            result = urllib.request.urlretrieve(url, filename)
            time.sleep(2)
        except Exception as e :
            print(e)

def get_md5(data):
    m = hashlib.md5()
    m.update(data)  # 参数必须是byte类型，否则报Unicode-objects must be encoded before hashing错误
    md5value = m.hexdigest()
    print(md5value)
    return md5value

def save(filename):
    try:
        fh = open(filename, 'a+')
    except Exception as e:
        print(e)
    finally:
        fh.close()

    return filename

def save_file(filename,bin):
    fh = open(filename, 'wb')
    fh.write(bin)
    fh.close()
    return filename

def handle_response(response):
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


if __name__ == '__main__':
    get_img()
    # get_code()