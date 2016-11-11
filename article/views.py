# -*- coding: utf-8 -*-
#操纵数据库,把数据库的数据返回给*.html，再将*.html返回给客户端
#from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.syndication.views import Feed
from django.core.paginator import Paginator, EmptyPage
from article.models import Article



# Create your views here.
def home(request):
    posts = Article.objects.all()  #获取全部的Article对象
    paginator = Paginator(posts, 4) #每页显示4篇文章
    #print(request)
    page = request.GET.get('page')
    if page != None:
        try :
            '''try:
                current_page = abs(int(page))
            except (ValueError, TypeError):
                raise Http404
            if current_page <= paginator._get_num_pages():
                post_list = paginator.page(current_page)
            else:
                raise Http404'''
            current_page = int(page)
            if current_page <= paginator._get_num_pages():
                post_list = paginator.page(current_page)
            else:
                raise Http404
        except (EmptyPage, ValueError, TypeError) :
            raise Http404
    else:
        post_list = paginator.page(1)
    return render(request, 'home.html', {'post_list' : post_list})

def detail(request, id):
    try:
        post = Article.objects.get(id=str(id))
        tags = post.tag.all()
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'post.html', {'post' : post, 'tags': tags})

def archives(request) :
    '''
    try:
        post_list = Article.objects.all()
    except Article.DoesNotExist :
        raise Http404
    '''
    post_list = Article.objects.all()
    return render(request, 'archives.html', {'post_list' : post_list})

def classification(request, article_class) :
    #post_list = Article.objects.filter(category__iexact = article_class) #contains
    post_list = Article.objects.filter(category=str(article_class))
    if list(post_list) != []:
        return render(request, 'class.html', {'post_list' : post_list})
    else:
        raise Http404

def about_me(request) :
    return render(request, 'aboutme.html')

def blog_search(request):
    if 's' in request.GET:
        s = request.GET['s']
        if not s:
            return render(request,'home.html')
        else:
            post_list = Article.objects.filter(title__icontains = s)
            if len(post_list) == 0 :
                return render(request,'archives.html', {'post_list' : post_list,
                                                    'error' : True})
            else :
                return render(request,'archives.html', {'post_list' : post_list,
                                                    'error' : False})
    return redirect('/')

class RSSFeed(Feed):
    title = "RSS feed - article"
    link = "feeds/posts/"
    description = "RSS feed - blog posts"

    def items(self):
        return Article.objects.order_by('-date_time')

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.date_time

    def item_description(self, item):
        return item.content
