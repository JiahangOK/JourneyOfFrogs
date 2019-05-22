import json
import time

from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect

from Frog import models


# 修改专员个人信息
def changeInfo(request):
    if request.method == 'GET':
        # print('来了老弟？')
        expert_name = request.GET['expert_name']
        expert_tel = request.GET['expert_tel']
        expert_intro = request.GET['expert_intro']
        expert_gender = request.GET['expert_gender']
        expert_seniority = request.GET['expert_seniority']
        expert_company = request.GET['expert_company']
        expert_tag = request.GET['expert_tag']

        v = request.session.get('expert_email')
        models.Expert.objects.filter(email=v).update(tag=expert_tag,
                                                     company=expert_company,
                                                     gender=expert_gender,
                                                     seniority=expert_seniority,
                                                     name=expert_name,
                                                     telephone=expert_tel,
                                                     introduction=expert_intro)
        res = {'cool': True}
        return HttpResponse(json.dumps(res), content_type='application/json')


# 修改密码
def changePassword(request):
    if request.method == 'GET':
        # print('来了老弟？')
        old_password = request.GET['old_password']
        new_password = request.GET['new_password']
        new_password_confirm = request.GET['new_password_confirm']
        res = {}
        v = request.session.get('expert_email')
        old_password_from_db = models.Expert.objects.get(email=v).password
        if old_password == old_password_from_db:
            if new_password == new_password_confirm:
                models.Expert.objects.filter(email=v).update(password=new_password)
                res['cool'] = True
                res['res_message'] = '修改密码成功!'
            else:
                res['cool'] = False
                res['res_message'] = '两次新密码不一致!'
        else:
            res['cool'] = False
            res['res_message'] = '旧密码不正确!'

        return HttpResponse(json.dumps(res), content_type='application/json')


# 查看历史订单
def expertOrderList(request):
    v = request.session.get('expert_email')
    if v:
        orders = models.Order.objects.filter(expert_id=v).exclude(state=0)
        return render(request, '../templates/expertOrderListPage.html', {'orders': orders})
    else:
        return redirect('/expert')




# 专员个人中心
def expert(request):
    if request.method == 'GET':
        # 输入的邮箱和密码
        email_input = "2973493373@qq.com"
        password = "123456"
        try:
            expert = models.Expert.objects.get(email=email_input, password=password)
        except models.Expert.DoesNotExist:
            expert = None

        if expert:
            # 登录成功返回页面
            request.session['expert_email'] = expert.email
            return render(request, '../templates/expertPage.html', {'expert': expert})
        else:
            return HttpResponse("用户名或者密码错误")
    elif request.method == 'POST':
        pass


# 服务订单
def orderHandling(request):
    v = request.session.get('expert_email')
    if v:
        orders = models.Order.objects.filter(expert_id=v, state=0)

        return render(request, '../templates/orderHandlingPage.html', {'orders': orders})
    else:
        return redirect('/expert')
