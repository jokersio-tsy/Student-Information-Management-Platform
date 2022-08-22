# -*- coding: utf-8 -*-
import email
import smtplib
from email.mime.text import MIMEText
import time
from turtle import up
import pymysql
from io import BytesIO

import qrcode
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import os
import uuid

import json
from app.models import Teacher, Student, Covid, Newcovid, Mail

from app.crawler import makeCovid
from app.confirm import get_confirm


def hello(request, name):
    return HttpResponse("hello "+name)


def register(request):
    if request.POST:
        # 获取6项信息 id 名字 密码 再确认密码 性别 大学
        id      = request.POST.get('tea_id', None)
        name    = request.POST.get('tea_name', None)
        paswd   = request.POST.get('password', None)
        p_a     = request.POST.get('password_again', None)
        gender  = request.POST.get('tea_gender', None)
        college = request.POST.get('college', None)

        if (paswd == p_a):
            teacher = Teacher(tea_id=id, college=college,
                              tea_gender=gender, tea_name=name, password=paswd)
            teacher.save()
            msg = '欢迎来自' + college + '的' + name
            rep = redirect('/app/login/')
            # 前端可以考虑在此处直接转到登录界面
            return rep
            # return HttpResponse(msg)
        else:
            msg = '密码不一致'
            return HttpResponse(msg)
    else:
        return render(request, 'login.html')


def login(request):
    if request.POST:
        # 接收客户端请求数据
        tea_id   = request.POST.get('tea_id', None)
        password = request.POST.get('password', None)

        # 处理请求（登录验证）
        # try寻找obj对象，若找不到不在数据库内，弹到except
        try:
            teacher = Teacher.objects.get(tea_id=tea_id)
            # 密码与数据库一致则登录成功
            if (teacher.password == password):
                # 将teacher主键数据：tea_id写入session,并且响应客户端
                request.session['tea_id'] = tea_id
                # print('session OK')

                rep = redirect('/app/homepage/')
                return rep

                # context = dict()
                # context['teacher'] = teacher
                # return render(request, 'homepage.html', context)

            else:
                return render(request, 'login.html', {'message': '账号密码错误'})

        except:
            return render(request, 'login.html', {'message': '账号不存在'})
    else:
        return render(request, 'login.html')
# 退出


def logout(request):
    # 删除当前登录者的session中的信息
    del request.session['tea_id']
    print('删除当前登录者的信息')
    # 重定向至登录页面
    return redirect('/app/login/')

# 教师端主页


def homepage(request):
    #print('------------------BEGIN')
    # # 获取session的数据
    id = request.session.get('tea_id', None)
    if not id:
        # 若未登录且试图直接使用url进入homepage，会跳转到登录页面
        return redirect('/app/login/')

    else:
        # # 调用函数实现按照主键进行查询检索
        obj = Teacher.objects.get(tea_id=id)
        context = dict()
        context['teacher'] = obj

        # 请求转发跳转至homepage页面
        # 在homepage页面显示欢迎信息
        # 若需要name外其他数据 通过obj进行抓取
        return render(request, 'homepage.html', context)


def getTeacherInfo(request):
    # 获取数据库中teacher信息
    teacher = Teacher.objects.all()
    # 把查询到的对象，封装到上下文
    context = {
        'teacher': teacher,
    }
    # 把上传文传到模板页面index.html里
    return render(request, 'teacherInfo.html', context)


def add_data_student(request):
    if(request.POST):
        stu_name        = request.POST.get('stu_name', None)
        stu_gender      = request.POST.get('stu_gender', None)
        pic             = request.POST.get('picFile', None)
        stu_id          = request.POST.get('stu_id', None)
        age             = request.POST.get('age', None)
        id              = request.POST.get('id', None)
        college         = request.POST.get('college', None)
        province        = request.POST.get('province', None)
        region          = request.POST.get('region', None)
        grade           = request.POST.get('grade', None)
        major           = request.POST.get('major', None)
        class_number    = request.POST.get('class_number', None)
        politics_statue = request.POST.get('politics_statue', None)
        phone           = request.POST.get('phone', None)
        email           = request.POST.get('email', None)
        area            = request.POST.get('area', None)

        x = area.split('/')
        province = x[0]
        region = x[1]
        area = x[2]

        covids = Covid.objects.all()
        riskArea = []
        for c in covids:
            riskArea.append(c.area)
        if area in riskArea:
            risk = 1
        else:
            risk = 0
        
        student = Student(area=area,risk=risk,stu_name=stu_name, stu_gender=stu_gender, pic=pic, id=id, college=college, stu_id=stu_id, age=age, province=province,\
                          region=region, grade=grade, major=major, class_number=class_number, politics_statue=politics_statue, phone=phone, email=email)
        student.save()
        # return render(request, 'information_getter_web.html', {'message': 'success'})

        
        return queryByCondition(request)

    else:
        return render(request, 'information_getter_web.html')


# 按照老师的学院查询学生信息---queryAll_by_college
def queryAll(request):
    # 从session获取老师的信息
    id  = request.session.get('tea_id', None)
    obj = Teacher.objects.get(tea_id=id)
    tea_college = obj.college

    students = Student.objects.all()
    students = students.filter(college=tea_college)
    context = dict()
    context['students'] = students

    return render(request, 'showStudents.html', context)


def queryByCondition(request):
    if(request.POST):
        students      = Student.objects.all()
        stu_id        = request.POST.get('stu_id', None)
        stu_gender    = request.POST.get('stu_gender', None)
        age           = request.POST.get('age', None)
        province      = request.POST.get('province', None)
        region        = request.POST.get('region', None)
        # area          = request.POST.get('area', None)
        grade         = request.POST.get('grade', None)
        college       = request.POST.get('college', None)
        major         = request.POST.get('major', None)
        class_number  = request.POST.get('class_number', None)
        politics_statue = request.POST.get('politics_statue', None)

        if stu_id:
            students = students.filter(stu_id=stu_id)
        if stu_gender:
            students = students.filter(stu_gender=stu_gender)
        if age:
            students = students.filter(age=age)
        if province:
            students = students.filter(province=province)
        if region:
            students = students.filter(region=region)
        # if area:
        #     students = students.filter(area=area)
        if grade:
            students = students.filter(grade=grade)
        if college:
            students = students.filter(college=college)
        if major:
            students = students.filter(major=major)
        if class_number:
            students = students.filter(class_number=class_number)
        if politics_statue:
            students = students.filter(politics_statue=politics_statue)

        context = dict()
        context['students'] = students
        return render(request, 'showStudents.html', context)

    else:
        return render(request, 'queryByCondition.html')

# 实现更新查询查询（get）


def preUpdate(request, stu_id):
    # 按照主键查询指定的部门信息
    student = Student.objects.get(stu_id=stu_id)
    # 将数据封装到传递参数中
    context = dict()
    context['student'] = student
    # 响应客户端（页面跳转）
    return render(request, 'update.html', context)


def update(request):
    if(request.POST):
        stu_name      = request.POST.get('stu_name', None)
        stu_gender    = request.POST.get('stu_gender', None)
        pic           = request.POST.get('picFile', None)
        stu_id        = request.POST.get('stu_id', None)
        age           = request.POST.get('age', None)
        id            = request.POST.get('id', None)
        college       = request.POST.get('college', None)
        province      = request.POST.get('province', None)
        region        = request.POST.get('region', None)
        grade         = request.POST.get('grade', None)
        major         = request.POST.get('major', None)
        class_number  = request.POST.get('class_number', None)
        politics_statue = request.POST.get('politics_statue', None)
        phone         = request.POST.get('phone', None)
        email         = request.POST.get('email', None)

        Student.objects.filter(stu_id=stu_id).update(stu_name=stu_name, stu_gender=stu_gender,
                                                     pic=pic, stu_id=stu_id, age=age, id=id, college=college, province=province, region=region,
                                                     grade=grade, major=major, class_number=class_number, politics_statue=politics_statue,
                                                     phone=phone, email=email)
        # 响应客户端
        return queryByCondition(request)


def delete(request, stu_id):
    # 调用删除函数
    Student.objects.filter(stu_id=stu_id).delete()
    # 响应客户端
    return queryAll(request)


# 图片上传业务实现
def picupload(request):
    # 接收客户端请求数据
    obj = request.FILES.get('file', None)
    # 处理请求数据
    # 获取上传图片的信息
    picFileName = obj.name
    picFileSize = obj.size
    picFileStuff = os.path.splitext(picFileName)[1]
    # 测试
    print('\n上传文件信息：')
    print('-' * 40)
    print('文件名称：{0}'.format(picFileName))
    print('文件大小：{0}'.format(picFileSize))
    print('文件后缀：{0}'.format(picFileStuff))
    # 创建可用文件类型列表
    allowedTypes = ['.png', '.jpg', '.gif', '.bmp', '.jpeg']
    # 判断上传文件类型是否受限
    if picFileStuff.lower() not in allowedTypes:
        print('文件类型不正确.')
        # 响应客户端
        return render(request, 'information_getter_web.html', {'error_msg': '错误：文件类型不正确，请您选择一张图片上传!'})
    # 生成唯一的文件名称
    picUploadUniqueName = str(uuid.uuid1()) + picFileStuff
    print('上传文件唯一名称：{0}'.format(picUploadUniqueName))
    # 验证上传文件夹
    uploadDirPath = os.path.join(os.getcwd(), 'app/static/image')
    if not os.path.exists(uploadDirPath):
        # 创建文件夹
        os.mkdir(uploadDirPath)
        print('服务器上传文件夹创建完毕.')
    else:
        print('服务器上传文件夹已存在.')
    # 设置上传文件的全路径
    picFileFullPath = uploadDirPath + os.sep + picUploadUniqueName
    print('上传文件全路径：{0}'.format(picFileFullPath))
    # 二进制文件写入操作
    try:
        # 获取文件的关联并生成文件操作对象fp
        with open(picFileFullPath, 'wb+') as fp:
            # 分割上传文件（当上传文件大小2.5MB以上是自动分割）
            for chunk in obj.chunks():
                fp.write(chunk)
            print('[OK] 上传文件写入服务器.')
    except:
        print('[Error] 上传文件写入服务器失败.')
        # 响应客户端
        return render(request, 'information_getter_web.html', {'error_msg': '[Error] 图片上传失败!'})
    # 响应客户端
    imgurl = '/static/image/' + picUploadUniqueName
    return HttpResponse(imgurl)

# 创建二维码


def makeqrcode(request):
    #注意别留空格
    img = qrcode.make(
        "https://962b-222-182-57-38.jp.ngrok.io/app/add_data_student/")  # 传入我们采集数据表单的网址
    buf = BytesIO()  # 创建一个BytesIO临时保存生成图片数据
    img.save(buf)  # 将图片字节数据放到BytesIO临时保存
    image_stream = buf.getvalue()  # 在BytesIO临时保存拿出数据
    response = HttpResponse(
        image_stream, content_type="image/jpg")  # 将二维码数据返回到页面
    return response

# 移动端跳转


def gotoinformation_getter_web(request):
    return render(request, 'information_getter_web.html')


#########################################################################################################
#以下函数实现了python连接数据库，并对里面学生发送email功能
# 从数据库中获取ip地址列表
def get_addr():
    # # 连接数据库
    conn = pymysql.connect(
    host='rm-2vcdr6ss506i2jmtb1o.mysql.cn-chengdu.rds.aliyuncs.com',
    user='team1',
    password='5tgb%TGB',
    db='db1',
    charset='utf8',
    # autocommit=True,如果插入数据，是否自动提交? 和conn.commit()功能一致。
    )
    #conn = pymysql.Connection('rm-2vcdr6ss506i2jmtb1o.mysql.cn-chengdu.rds.aliyuncs.com', 'team1', '5tgb%TGB', 'db1')
    cursor = conn.cursor()
    # 执行SQL语句，获取邮箱地址
    cursor.execute("SELECT * FROM mail")
    result = cursor.fetchall()
    return result

# 发送邮件
def send_mail(request, to_list):
    mail_server     = "smtp.163.com"    # 邮箱host
    mail_port       = 25                # 端口号
    sender          = "team1_project@163.com"   # 自己的邮箱账号
    sender_password = "HXSWRPWMITWBFVQG"  # 授权码,不是账号密码
    receivers       = to_list     # 对方的邮箱账号

    #session获取发件人：老师的信息
    id  = request.session.get('tea_id', None)
    obj = Teacher.objects.get(tea_id=id)
    print('0000')
    # context = dict()
    # context['teacher'] = obj

    # 邮件内容
    # 实现在前端页面自定义发送邮件
    msg = request.POST.get('content', None)
    print('0001')
    # message = MIMEText('This is the test email sent to you by Team 1, please check it carefully...\n \
    #     可视化云图：Href：https://v.yuntus.com/tcv/3859CeD2b1Ea7D471F9e3D7c13339BF0 \n \
    #         PS:可以通过session写入发件人（当前登录的老师） + 将收件人学生的信息在邮件中展示，可能要写html邮件', 'plain', 'utf-8')
    print(msg)

    message = MIMEText(msg)
    message['From'] = sender      # 发送者
    message['To']   = receivers   # 接受者

    # 设置邮件的主题
    send_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    
    #将主题表现为发件人老师来信
    subject   = obj.college +'的'+ obj.tea_name +'老师来信' + send_time
    print(subject)
    message['Subject'] = subject

    try:
        smtp_obj = smtplib.SMTP()
        smtp_obj.connect(mail_server, mail_port)    # 连接邮箱的服务器
        smtp_obj.login(sender, sender_password)     # 登录自己的邮箱
        smtp_obj.sendmail(sender, [receivers], message.as_string())     # 真正开始发送邮件
        print('success!')
    except smtplib.SMTPException as e:
        print('failure!')
        print(e)

#实现从数据库中获取邮箱地址发送邮件
def sendEmail(request):
    if request.POST:
        result = get_addr()
        for record in result:
            send_mail(request, record[1])

            # 休眠1秒，短时间大量发送邮件可能会造成发送失败或者账号被封
            time.sleep(1)
        return HttpResponse('邮件群发成功！！！')
    else:
        return render(request, 'testEmail.html')
        # 也可以直接填写对方的邮箱账号
        # send_mail("XXXX@163.com")


#实现从前端勾选框checked对象发送邮件
def gotosendemail(request):
    #json格式
    datas = request.body
    datas = json.loads(datas)
    print(datas)
    #先清空mail表的数据库信息
    Mail.objects.all().delete()

    #将勾选的学生信息存储到mail：数据库
    for var in datas:
        id = var['stu_id']
        id = int(id)
        print(id)
        stu  = Student.objects.get(stu_id=id)
        email = stu.email
        print(email)
        mail = Mail(stu_id=id,email=email)
        print(mail)
        mail.save()
    print('在跳转页面之前------------------------------')
    return render(request, 'testEmail.html')
    #return sendEmail

#进入自由编辑邮件的页面
def testEmail(request):
    return render(request, 'testEmail.html')

##################################################################################
#测试运行后更新数据库
#从网页中爬取疫情风险地区，并保存到数据库的Covid表
# TIPS：用的某博主的API 他的密钥和代理 这样自己爬取网页的时候就避免了输入账户密码的问题
# Waring：短时间多次运行可能IP被当作恶意攻击，导致无法进行数据爬取

# import hashlib
# import json
# import difflib
# import requests
# import time
# import pymysql


# timestamp = str(int((time.time())))
# # print(timestamp)

# token = '23y0ufFl5YxIyGrI8hWRUZmKkvtSjLQA'
# nonce = '123456789abcdefg'
# passid = 'zdww'
# key = "3C502C97ABDA40D0A60FBEE50FAAD1DA"


# def get_zdwwsignature():
#     zdwwsign = timestamp + 'fTN2pfuisxTavbTuYVSsNJHetwq5bJvC' + \
#         'QkjjtiLM2dCratiA' + timestamp
#     hsobj = hashlib.sha256()
#     hsobj.update(zdwwsign.encode('utf-8'))
#     zdwwsignature = hsobj.hexdigest().upper()
#     # print(zdwwsignature)
#     return zdwwsignature


# def get_signatureheader():
#     has256 = hashlib.sha256()
#     sign_header = timestamp + token + nonce + timestamp
#     has256.update(sign_header.encode('utf-8'))
#     signatureHeader = has256.hexdigest().upper()
#     # print(signatureHeader)
#     return signatureHeader


# def get_datas():
#     url = 'https://bmfw.www.gov.cn/bjww/interface/interfaceJson'
#     headers = {
#         "Accept": "application/json, text/javascript, */*; q=0.01",
#         "Accept-Encoding": "gzip, deflate, br",
#         "Accept-Language": "zh-CN,zh;q=0.9",
#         "Connection": "keep-alive",
#         # "Content-Length": "235",
#         "Content-Type": "application/json; charset=UTF-8",
#         "Host": "bmfw.www.gov.cn",
#         "Origin": "http://bmfw.www.gov.cn",
#         "Referer": "http://bmfw.www.gov.cn/yqfxdjcx/risk.html",
#         # "Sec-Fetch-Dest": "empty",
#         # "Sec-Fetch-Mode": "cors",
#         # "Sec-Fetch-Site": "cross-site",
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 SE 2.X MetaSr 1.0",
#         "x-wif-nonce": "QkjjtiLM2dCratiA",
#         "x-wif-paasid": "smt-application",
#         "x-wif-signature": get_zdwwsignature(),
#         "x-wif-timestamp": timestamp
#     }

#     params = {
#         'appId': "NcApplication",
#         'paasHeader': "zdww",
#         'timestampHeader': timestamp,
#         'nonceHeader': "123456789abcdefg",
#         'signatureHeader': get_signatureheader(),
#         'key': "3C502C97ABDA40D0A60FBEE50FAAD1DA"
#     }

#     resp = requests.post(url, headers=headers, json=params)
#     datas = resp.text
#     # print('---------------------------------------------------------------')
#     # print(datas)
#     return datas

# #抓取高风险地区数据
# def get_highlist(data):
#     highlist = data['data']['highlist']
#     return highlist

# #高风险地区数据更新到数据库
# def update_high_lst(data):
#     for obj in data:
#         addr = obj['county']
#         print(addr)
#         var  = Covid(area=addr, risk='高')
#         var.save()
#     return

# #抓取中风险地区数据
# def get_middlelist(data):
#     middlelist = data['data']['middlelist']
#     return middlelist

# #中风险地区数据更新到数据库
# def update_mid_lst(data):
#     for obj in data:
#         addr = obj['county']
#         print(addr)
#         var  = Covid(area=addr, risk='中')
#         var.save()
#     return

# #抓取低风险地区数据
# def get_lowlist(data):
#     lowlist = data['data']['lowlist']
#     return lowlist

# #低风险地区数据更新到数据库
# def update_low_lst(data):
#     for obj in data:
#         addr = obj['county']
#         print(addr)
#         var  = Covid(area=addr, risk='低')
#         var.save()
#     return


# #疫情风险地区爬取及更新到数据库的主函数
# def makeCovid(request):
#     datas     = get_datas()              #从网页爬取数据
#     datas_dic = json.loads(datas)        #将数据从json转化为python格式

#     if datas:
#         #先清空数据库中Covid表原有数据
#         Covid.objects.all().delete()

#         #高风险、中风险、低风险
#         high_lst  = get_highlist(datas_dic)
#         update_high_lst(high_lst)
#         mid_lst   = get_middlelist(datas_dic)
#         update_mid_lst(mid_lst) 
#         low_lst   = get_lowlist(datas_dic)
#         update_low_lst(low_lst)

#     else:
#         return HttpResponse("ERROR HAPPENED")
#     #前端可以编辑页面 后端可以在此处直接跳转到zmh负责的腾讯云图
#     return HttpResponse("OK!")


# #########################################################################################################
#给学生设置risk判断是否在风险区
def setRisk(request):
    #print(now())
    students = Student.objects.all()
    covids = Covid.objects.all()
    riskArea = []
    for c in covids:
        riskArea.append(c.area)
    print(len(riskArea))

    riskArea = list(set(riskArea))
    print(len(riskArea))

    cnt=0
    rr=[]
    for stu in students:
        if stu.area in riskArea:
            Student.objects.filter(stu_id=stu.stu_id).update(risk=1)
            cnt+=1
            rr.append(stu.area)
        else:
            Student.objects.filter(stu_id=stu.stu_id).update(risk=0)

    rr = list(set(rr))
    print('cnt', cnt)
    print('rr', rr)
    print('rrlen', len(rr))

    #print(now())

def queryRisk(request):
    #print(now())
    # 从session获取老师的信息
    id = request.session.get('tea_id', None)
    obj = Teacher.objects.get(tea_id=id)
    tea_college = obj.college

    students = Student.objects.filter(college=tea_college)
    students = Student.objects.filter(risk=1)

    context = dict()
    context['students'] = students
    return render(request, 'showRiskStudents.html', context)

def gotoepidemic_ctrl(request):
    return render(request, 'epidemic_ctrl.html')



