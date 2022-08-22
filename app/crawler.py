##################################################################################
# 测试运行后更新数据库
# 从网页中爬取疫情风险地区，并保存到数据库的Covid表
# TIPS：用的某博主的API 他的密钥和代理 这样自己爬取网页的时候就避免了输入账户密码的问题
# Waring：短时间多次运行可能IP被当作恶意攻击，导致无法进行数据爬取

import hashlib
import json
import difflib
import requests
import time
import pymysql
from app.models import Covid, High, Middle, Low
from django.http import HttpResponse

timestamp = str(int((time.time())))
print('timestamp:' + timestamp)
token = '23y0ufFl5YxIyGrI8hWRUZmKkvtSjLQA'
nonce = '123456789abcdefg'
passid = 'zdww'
key = "3C502C97ABDA40D0A60FBEE50FAAD1DA"


def get_zdwwsignature():
    zdwwsign = timestamp + 'fTN2pfuisxTavbTuYVSsNJHetwq5bJvC' + \
        'QkjjtiLM2dCratiA' + timestamp
    hsobj = hashlib.sha256()
    hsobj.update(zdwwsign.encode('utf-8'))
    zdwwsignature = hsobj.hexdigest().upper()
    # print(zdwwsignature)
    return zdwwsignature


def get_signatureheader():
    has256 = hashlib.sha256()
    sign_header = timestamp + token + nonce + timestamp
    has256.update(sign_header.encode('utf-8'))
    signatureHeader = has256.hexdigest().upper()
    # print(signatureHeader)
    return signatureHeader


def get_datas():
    url = 'https://bmfw.www.gov.cn/bjww/interface/interfaceJson'
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        # "Content-Length": "235",
        "Content-Type": "application/json; charset=UTF-8",
        "Host": "bmfw.www.gov.cn",
        "Origin": "http://bmfw.www.gov.cn",
        "Referer": "http://bmfw.www.gov.cn/yqfxdjcx/risk.html",
        # "Sec-Fetch-Dest": "empty",
        # "Sec-Fetch-Mode": "cors",
        # "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 SE 2.X MetaSr 1.0",
        "x-wif-nonce": "QkjjtiLM2dCratiA",
        "x-wif-paasid": "smt-application",
        "x-wif-signature": get_zdwwsignature(),
        "x-wif-timestamp": timestamp
    }

    params = {
        'appId': "NcApplication",
        'paasHeader': "zdww",
        'timestampHeader': timestamp,
        'nonceHeader': "123456789abcdefg",
        'signatureHeader': get_signatureheader(),
        'key': "3C502C97ABDA40D0A60FBEE50FAAD1DA"
    }
    print(0)
    resp = requests.post(url, headers=headers, json=params)
    print(resp.status_code)
    datas = resp.text

    return datas

# 抓取高风险地区数据


def get_highlist(data):
    highlist = data['data']['highlist']
    return highlist

# 高风险地区数据更新到数据库


def update_high_lst(data):
    for obj in data:
        province = obj['province']
        if (province == '北京市'):
            region = province
            area = obj['city']

        else:
            region = obj['city']
            area = obj['county']
        var1 = Covid(area=area, risk='高')
        var2 = High(province=province, region=region, area=area)
        var1.save()
        var2.save()
    print('爬取更新高风险地区数据完成')
    return

# 抓取中风险地区数据


def get_middlelist(data):
    middlelist = data['data']['middlelist']
    return middlelist

# 中风险地区数据更新到数据库


def update_mid_lst(data):
    for obj in data:
        province = obj['province']
        if (province == '北京市'):
            region = province
            area = obj['city']
        else:
            region = obj['city']
            area = obj['county']
        var1 = Covid(area=area, risk='中')
        var2 = Middle(province=province, region=region, area=area)
        var1.save()
        var2.save()
    print('爬取更新中风险地区数据完成')
    return

# 抓取低风险地区数据


def get_lowlist(data):
    lowlist = data['data']['lowlist']
    return lowlist

# 低风险地区数据更新到数据库


def update_low_lst(data):
    for obj in data:
        province = obj['province']
        if province == '北京市':
            region = province
            area = obj['city']
        else:
            region = obj['city']
            area = obj['county']
        var1 = Covid(area=area, risk='低')
        var2 = Low(province=province, region=region, area=area)
        var1.save()
        var2.save()
    print('爬取更新低风险地区数据完成')
    return


# 疫情风险地区爬取及更新到数据库的主函数
def makeCovid(request):
    print('开始爬取。。。。')
    timestamp = str(int((time.time())))
    print('爬取时间：'+timestamp)
    try:  # 爬取成功，返回True
        datas = get_datas()  # 从网页爬取数据
        datas_dic = json.loads(datas)  # 将数据从json转化为python格式
        # 先清空数据库中Covid表原有数据
        print("正常运行1")
        # High.objects.all().delete()
        # Middle.objects.all().delete()
        # Low.objects.all().delete()
        # 高风险、中风险、低风险
        high_lst = get_highlist(datas_dic)
        print("正常运行2")
        Covid.objects.all().delete()
        High.objects.all().delete()
        update_high_lst(high_lst)
        mid_lst = get_middlelist(datas_dic)
        Middle.objects.all().delete()
        update_mid_lst(mid_lst)
        low_lst = get_lowlist(datas_dic)
        Low.objects.all().delete()
        update_low_lst(low_lst)
        print("爬取风险地区数据成功！！！")
        get_time = datas_dic['data']['end_update_time']
    # 前端可以编辑页面 后端可以在此处直接跳转到zmh负责的腾讯云图
        return HttpResponse('数据更新成功！！！' + '该数据更新时间为：' + get_time)
    except Exception as e:
        print(e)
        return HttpResponse('数据更新失败。。。请稍后再试')
