from django.shortcuts import render, redirect, HttpResponse
import time
from django.conf import settings
from . import models
# Create your views here.
import json
# 分享攻略


def share(request):
    if request.method == "GET":
        return render(request, '../templates/complete/shareStrategyPage.html')
    if request.method == "POST":
        print(request.POST)

        member = models.Member.objects.get(email=request.user)
        content = request.POST.get('content')
        title = request.POST.get('title')
        cover = request.POST.get('cover')
        peopleNumber = request.POST.get('peopleNumber')
        budget = request.POST.get('budget')
        days = request.POST.get('days')

        print(cover)
        newstrategy = models.Strategy.objects.create(peopleNumber=peopleNumber, budget=budget, content=content,
                                                     memberEmail=member, strategyTitle=title,
                                                     coverUrl=cover, days=days)

        print(newstrategy)
        print(newstrategy.strategyId)
        articleurl = '/article/' + str(newstrategy.strategyId)
        return redirect(articleurl)

        # print(request.POST)
        # return render(request, '../templates/complete/shareStrategyPage.html')


def detailArticle(request, strategyId):
    print("######################")
    print(strategyId)
    # useremail = 1 # 假定用户邮箱
    useremail = request.user
    member = models.Member.objects.get(email=useremail)

    digg_tag = 0  # 初始点赞状态
    if request.method == "GET":
        if not models.Strategy.objects.filter(strategyId=strategyId):
            error = "strategy not found"
            return redirect('/index')
            # return render(request, '../templates/complete/article.html', {'error': error})

    strategy = models.Strategy.objects.get(strategyId=strategyId)
    if request.method == "POST":
        commentcontent = request.POST.get("commentContent")
        print(commentcontent)
        models.Comment.objects.create(useremail=member, content=commentcontent, strategy=strategy)

    if models.Digg.objects.filter(useremail=member, strategy=strategy):
        digg_tag = 1

    comments = models.Comment.objects.filter(strategy=strategy).order_by('-commentId')
    return render(request, '../templates/complete/strategyDetailPage.html', {'strategy': strategy, 'comments': comments,
                                                                             'digg_tag': digg_tag})


def singleUser(request, userId):
    print(userId)
    user_email = request.user
    u = models.Member.objects.get(email=user_email)
    if models.User.objects.filter(id=userId):
        user = models.User.objects.get(id=userId)
        if user.type == '普通用户':
            member = models.Member.objects.get(email=user.username)
            fan_number = models.Follow.objects.filter(followedEmail=member).count()
            tag = 0
            if models.Follow.objects.filter(followedEmail=member, followingEmail=u):
                tag = 1
            return render(request, '../templates/complete/singleUserPage.html', {'member': member,
                                                                                 'email': json.dumps(member.email),
                                                                                 'fan_number': fan_number,
                                                                                 'tag': tag})

    return redirect('/index')


# 图片上传接口
def getimage(request):
    pic = request.FILES.get('file')
    uid = request.POST.get('uid')
    ct = time.time()
    date_head = 'IMG_' + str(time.strftime("%Y%m%d_%H%M%S", time.localtime()))
    date_secs = (ct - int(ct)) * 1000
    filename = "%s_%03d" % (date_head, date_secs) + '.jpg'
    save_path = '%s%s' % (settings.IMG_ROOT, filename)  # pic.name 上传文件的源文件名
    print(save_path)
    with open(save_path, 'wb') as f:
        # 3.获取上传文件的内容并写到创建的文件中
        for content in pic.chunks():  # pic.chunks() 上传文件的内容。
            f.write(content)
    return HttpResponse(str(filename))


# 点赞接口
def digg(request):
    # 差把保存点赞
    useremail = request.user
    member = models.Member.objects.get(email=useremail)
    if request.method == "GET":
        strategy = models.Strategy.objects.get(strategyId=request.GET.get('strategyId'))
        if models.Digg.objects.filter(useremail=member, strategy=strategy):
            models.Digg.objects.get(useremail=member, strategy=strategy).delete()
            return HttpResponse(0)
        else:
            models.Digg.objects.create(useremail=member, strategy=strategy)
            return HttpResponse(1)
    else:
        return HttpResponse(-1)


def follow(request):
    print(request)
    print(request.user)
    print(request.GET)
    fan = models.Member.objects.get(email=request.user)
    follow_email = request.GET.get('followEmail')
    follow = models.Member.objects.get(email=follow_email)

    if models.Follow.objects.filter(followedEmail=follow, followingEmail=fan):
        models.Follow.objects.get(followedEmail=follow, followingEmail=fan).delete()
        return HttpResponse(1)
    else:
        models.Follow.objects.create(followedEmail=follow, followingEmail=fan)
        return HttpResponse(0)