# coding:utf-8

from mongoengine import *
from testDjango.apps.models import *



def test_mongo():
    conn = connect('test')
    respondent = Respondents()
    print(type(respondent))
    respondent.cell_num = '111'
    c = {'d':'d','e':'e'}
    respondent.info = {'a':1,'b':'b','c':c}
    inner = Inner()
    inner.name = 'nn'
    inner.l = [1,2,3,4]
    respondent.inner = inner
    inner.save()
    respondent.save()


    rs = Respondents.objects.filter(cell_num='111')
    print(len(rs))
    print(rs)
    for i in rs:
        print(type(i))
        temp = {'haha':'jaja'}
        i.info.update(temp)
        print(i.to_json())
        i.save()





if __name__ == '__main__':
    test_mongo()
