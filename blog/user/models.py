#coding=utf-8
from django.db import models
class UserInfo(models.Model):
    username = models.CharField(max_length=20)
    userpassword = models.CharField(max_length=40)
    useremail = models.CharField(max_length=30,default='')
    userphone = models.CharField(max_length=11)
    userpic = models.ImageField(upload_to='user',default='/static/images/default.png')
# Create your models here.
