from django.core.paginator import  Paginator,Page
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Artical
from user.models import UserInfo
from django.db.models import Q

@csrf_exempt
def index(request,sort,pindex):
    hotest = Artical.objects.filter().order_by('-click')[0:3]
    article_list = []
    if sort == '1':
        article_list = Artical.objects.filter().order_by('-modifydate')
        print(article_list)
    elif sort == '2':
        article_list = Artical.objects.filter().order_by('-click')
        print(article_list)
    paginator = Paginator(article_list, 10)
    page = paginator.page(int(pindex))
    maxpage = int(len(article_list)/10)+1
    context = {
        'page':page,
        'hotest':hotest,
        'sort':sort,
        'pindex':pindex,
        'maxpage':maxpage,
    }
    return render(request,'user_articles/index.html',context)

def detail(request,aid):
    article = Artical.objects.get(pk=int(aid))
    user = article.uid
    author =UserInfo.objects.get(pk=int(user.id))
    article.click = article.click + 1
    article.save()
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
        'words':words,
    }
    return render(request, 'user_articles/search.html', context)

