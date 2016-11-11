# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from article import views
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'my_blog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^my_admin/', include(admin.site.urls)),  #后台管理
    url(r'^$', 'article.views.home', name = 'home'),  #主页
    url(r'^(?P<id>\d+)/$', 'article.views.detail', name='detail'), #文章内容
    url(r'^archives/$', 'article.views.archives', name = 'archives'), #文章归档
    url(r'^aboutme/$', 'article.views.about_me', name = 'about_me'),  #关于我
    url(r'^class/(?P<article_class>\w+)/$', 'article.views.classification', name = 'classification'), #分类
    url(r'^search/$','article.views.blog_search', name = 'search'),   #搜索
    url(r'^feed/$', views.RSSFeed(), name = "RSS"),
    #url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_ROOT}),


)
"""
修改下 index() 视图， 让它显示系统中最新发布的 5 个调查问题，以逗号分割并按发布日期排序：:

from django.http import HttpResponse

from polls.models import Poll

def index(request):
    latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
    output = ', '.join([p.question for p in latest_poll_list])
    return HttpResponse(output)
"""