# coding=utf-8
import os


from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect

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
       # s1 = sha1()
        #s1.update(str(userpassword).encode('utf-8'))
        #s1.hexdigest()
        if userpassword == users[0].userpassword:
            url = request.COOKIES.get('url', '/')  # 从cookie中取出url完整路径参照user_decorator
            request.session['user_id'] = users[0].id  # 用于user_decorator传用户id验证是否登录
            request.session['userphone'] = userphone
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


def logout(request):
    request.session.flush()
    return redirect('/')

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
def articles(request,pindex):
    uid = request.COOKIES.get('user_id')
    article_list = Artical.objects.filter(uid=uid).order_by('-createdate')
    maxpage = article_list.count()/10
    paginator = Paginator(article_list, 10)
    page = paginator.page(int(pindex))
    context = {
        'page': page,
        'paginator': paginator,
        'pindex': pindex,
        'maxpage':maxpage,
    }
    return render(request,'user/articles.html',context)

# 展示用户文章内容&修改
@csrf_exempt
def detail(request,pid):
    article = Artical.objects.get(pk=int(pid))
    if request.method == "POST":
        article.title = request.POST.get('title')
        article.content = request.POST.get('content')
        article.save()
    context = {
        'article':article
    }
    return render(request,'user/userart_detail.html',context)

# 删除文章
def article_delete(request,aid):
    try:
        article = Artical.objects.get(pk=int(aid))
        article.delete()
        data = {'ok': 1}
    except Exception as e:
        data = {'ok': 0}
    return render(request,'user/articles.html')




