import time
import json
import requests
from datetime import datetime

import numpy as np

from app.models import Newcovid
from django.http import HttpResponse


def get_data():
    url = 'https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?adCode=500000&limit=30'
    response = requests.get(url)
    datas = response.text
    return datas


def get_covid(data):
    try:
        for obj in data:
            if(obj['confirm'] >= 785):
                year = obj['year']
                date = obj['date']
                month, day = date.split('.', 1)
                date1 = str(year) + '-' + month + '-' + day
                confirm = obj['confirm'] - obj['heal'] - obj['dead']
                confirm_add = obj['all_local_confirm_add']
                wzz = obj['wzz']
                wzz_add = obj['wzz_add']
                print(date1)
                var = Newcovid(time=date1, confirm=confirm,
                               confirm_add=confirm_add, wzz=wzz, wzz_add=wzz_add)
                # print(var)
                var.save()
        print("重庆疫情数据更新完毕")
        message = "success"
        return message
    except Exception as e:
        print(e)
        print("重庆疫情数据更新失败")
        message = "failure"
        return message


def get_confirm(request):
    datas = get_data()
    data = json.loads(datas)
    data = data['data']
    message = get_covid(data)
    print("Ok!")
    return HttpResponse(message)
