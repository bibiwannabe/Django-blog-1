# coding=utf-8
import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect
from .import login_decorator
from blog import settings
from .models import UserInfo
from hashlib import sha1
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from user_articles.models import Artical
from django.core.paginator import Paginator
from . import models


@csrf_exempt
def login(request):
    username = request.COOKIES.get('username', '')
    context = {
        'error_name': 0,
        'error_pwd': 0,
        'username': username,
    }
    return render(request,'user/login_1.html', context)

@csrf_exempt
def login_handle(request):
    post = request.POST
    userphone = post.get('phone')
    print(userphone)
    userpassword = post.get('password')
    print(userpassword)
    users = UserInfo.objects.filter(userphone=userphone)
    if len(users) == 1:
        print(userphone)
       # s1 = sha1()#此部分可用于用户密码加密
        #s1.update(str(userpassword).encode('utf-8'))
        #s1.hexdigest()
        if userpassword == users[0].userpassword:
            url = request.COOKIES.get('url', '/')  # 从cookie中取出url完整路径参照user_decorator
            request.session['user_id'] = users[0].id  # 用于user_decorator传用户id验证是否登录
            request.session['user_name'] = users[0].username #用于显示导航栏‘欢迎您，{{request.session.user_name}}’
            print('ss')
            context = 0
            return HttpResponse(context)
        else:
            context = 2
            print(context)
            return HttpResponse(context)
    else:
        context = 1
        print(context)
        return HttpResponse(context)

#退出登录 返回主页
def logout(request):
    request.session.flush()
    return redirect('/index_1_1/')

#注册
def  register(request):
    context={
        'register':1,
    }
    return render(request, 'user/login_1.html')

@csrf_exempt
def register_handle(request):
    post = request.POST
    username = post.get('phone')
    userphone = post.get('phone')
    userpassword=post.get('password')
#    cuserpassword = post.get('cpwd')
#    if userpassword != cuserpassword:
 #       return redirect('/user/register/')
    #密码加密
#    s1 = sha1()
#    s1.update(str(userpassword).encode('utf-8'))
#    upwd = s1.hexdigest()
    #创建对象
    user = UserInfo()
    user.userphone= userphone
    user.username = username
    print(username)
    user.userpassword = userpassword
    user.save()
    context = 0
    return HttpResponse(context)

#用户已经存在
def register_exist(request):
    username = request.GET.get('username')
    count = models.UserInfo.objects.filter(username=username).count()
    return JsonResponse({'count':count})

#用户信息页展示
@login_decorator.login#此为位于login_decorator.py下的验证登录装饰器 用于防止用户登陆之前访问到可修改信息的界面
def info(request):
    uid = request.session['user_id']
    user = UserInfo.objects.get(pk=int(uid))
    if request.method == "POST":
        user.username = request.POST.get('username')
        user.useremail = request.POST.get('useremail')
        user.userpic = request.FILES.get('userpic')
        user.save()
    context = {
        'user':user,
    }
    return render(request, 'user/info.html', context)

# 我的文章 展示用户文章列表
@login_decorator.login
def articles(request,sort,pindex):
    uid = request.session['user_id']
    user = UserInfo.objects.get(pk=int(uid))
    article_list = []
    if sort =='1':
        article_list = Artical.objects.filter(uid=user).order_by('-createdate')
    if sort =='2':
        article_list = Artical.objects.filter(uid=user).order_by('-click')
    print(article_list)
    maxpage = len(article_list)/10+1
    paginator = Paginator(article_list, 10)
    page = paginator.page(int(pindex))
    context = {
        'page': page,
        'pindex': pindex,
        'maxpage':maxpage,
    }
    return render(request,'user/articles.html',context)

# 展示用户文章内容&修改
@login_decorator.login
@csrf_exempt
def detail(request,aid):
    article = Artical.objects.get(pk=int(aid))
    if request.method == "POST":
        article.title = request.POST.get('title')
        article.content = request.POST.get('content')
        article.save()
    context = {
        'article':article,
        'create':0,
    }
    return render(request,'user/userart_detail.html',context)

# 删除文章
@login_decorator.login
def article_delete(request,aid):
    try:
        article = Artical.objects.get(pk=int(aid))
        article.delete()
        data = {'ok': 1}
    except Exception as e:
        data = {'ok': 0}
    return render(request,'user/articles.html')

#创建文章
@login_decorator.login
def create_article(request):
    context = {
        'create':1,
    }
    return render(request,'user/userart_detail.html',context)

#创建文章操作
@login_decorator.login
def creat_handle(request):
    post = request.POST
    title = post.get('title')
    content = post.get('content')
    article = Artical()
    article.content = content
    article.title = title
    article.click = 0
    uid = request.session['user_id']
    article.uid = UserInfo.objects.get(pk=int(uid))
    article.save()
    context = {
        'article':article,
    }
    return redirect('/user/userart_'+str(article.id)+'/')

def head(request):
    return render(request,'8.html')




