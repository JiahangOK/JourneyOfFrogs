from django.db import models


# Create your models here.

# -------------------- wjh models begin --------------------
class Expert(models.Model):
    email = models.EmailField(primary_key=True)

    name = models.CharField(max_length=10)
    password = models.CharField(max_length=64)
    gender = models.CharField(max_length=10)
    telephone = models.CharField(max_length=11)

    introduction = models.TextField()
    seniority = models.IntegerField()
    tag = models.CharField(max_length=10)
    company = models.CharField(max_length=64)
    mark = models.FloatField()


class Member(models.Model):
    email = models.EmailField(primary_key=True)

    name = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    gender = models.CharField(max_length=64)
    telephone = models.CharField(max_length=64)

    location = models.CharField(max_length=64)
    followNum = models.IntegerField()
    fansNum = models.IntegerField()


class Order(models.Model):
    member = models.ForeignKey(db_column='member_email', to=Member, on_delete=models.CASCADE)
    expert = models.ForeignKey(db_column='expert_email', to=Expert, on_delete=models.CASCADE)
    state = models.IntegerField()
    date = models.DateTimeField(null=True)
    intent = models.TextField(null=True)
    comment = models.TextField(null=True)
    mark = models.FloatField(null=True)
# -------------------- wjh models end --------------------

class User(models.Model):
    '''用户表'''
    # email = models.ForeignKey(max_length=30,unique=True)
    email = models.ForeignKey(max_length=30, unique=True)
    name = models.CharField(max_length=10)
    password = models.CharField(max_length=64)
    gender = models.IntegerField(max_length=32, default='男')
    telephone = models.IntegerField()


# 攻略表
class Strategy(models.Model):
    strategyId = models.AutoField(primary_key=True)
    peopleNumber = models.IntegerField(blank=True, null=True, default=0)
    budget = models.BigIntegerField(blank=True, null=True)
    content = models.CharField(max_length=500, blank=True, null=True)
    strategyTitle = models.CharField(max_length=10, blank=True, null=True)


# 评论表
class Comment(models.Model):
    commentId = models.AutoField(primary_key=True)
    useremail = models.CharField(max_length=100, blank=True, null=True)
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)
    time = models.DateField(auto_now_add=True, blank=True, null=True)
    content = models.CharField(max_length=500, blank=True, null=True)


# 点赞表
class Digg(models.Model):
    useremail = models.CharField(max_length=100, blank=True, null=True)
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)