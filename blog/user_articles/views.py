from django.core.paginator import  Paginator
from django.shortcuts import render
from .models import Artical
from user.models import UserInfo
from django.db.models import Q
def index(request,sort,pindex):
    hotest = Artical.objects.filter().order_by('-click')[0:3]
    if sort == 1:
        article_list = Artical.objects.filter().order_by('-modifydate')
    elif sort == 2:
        article_list = Artical.objects.filter().order_by('-click')
    paginator = Paginator(article_list, 10)
    page = paginator.page(int(pindex))
    maxpage = article_list.count()/10
    context = {
        'page':page,
        'paginator':paginator,
        'hotest':hotest,
        'pindex':pindex,
        'maxpage':maxpage,
    }
    return render(request,'user_articles/index.html',context)

def detail(request,aid):
    article = Artical.objects.get(pk=int(aid))
    author =UserInfo.objects.get(pk=int(article.uid))
    context = {
        'article':article,
        'author':author,
    }
    return render(request,'user_articles/detail.html',context)

def search(request,pindex):
    words = request.GET.get('words')
    article_list = Artical.objects.filter(Q(title__icontains=words)|Q(content__icontains=words))
    article_num = article_list.count()
    maxpage = article_num/10
    paginator = Paginator(article_list, 10)
    page = paginator.page(int(pindex))
    context = {
        'page': page,
        'paginator': paginator,
        'maxpage':maxpage,
        'pindex':pindex,
    }
    return render(request, 'user_articles/index.html', context)

