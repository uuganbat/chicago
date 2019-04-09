# !/usr/bin/python/env
# -*- coding:utf-8 -*-

from app import Nurl
from django.conf.urls import url

import views as v

urlpatterns = [
	Nurl(r'^$') > 'articles.views.List',
	Nurl(r'^c/(?P<slug>.+)/$') > 'articles.views.List',
	Nurl(r'^detail/(?P<pk>.+)/$') > 'articles.views.Detail',
	Nurl(r'^create/$') > 'articles.views.Create',
	url(r'^comment/(?P<pk>.+)/$', v.comment, name = 'article-comment'),
	url(r'^reply/(?P<pk>.+)/$', v.reply, name = 'article-reply'),
]