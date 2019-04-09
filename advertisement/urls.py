# !/usr/bin/python/env
# -*- coding:utf-8 -*-

from app import Nurl
from django.conf.urls import url
import views as v


urlpatterns = [
	
	Nurl(r'^$') > 'advertisement.views.List',
	Nurl(r'^c/(?P<slug>.+)/$') > 'advertisement.views.List',
	Nurl(r'^create/$') > 'advertisement.views.Create',
	Nurl(r'^update/(?P<pk>.+)/$') > 'advertisement.views.Update',
	Nurl(r'^detail/(?P<pk>.+)/$') > 'advertisement.views.Detail',
	Nurl(r'^save/(?P<pk>.+)/$') > 'advertisement.views.Save',
	Nurl(r'^remove/(?P<pk>.+)/$') > 'advertisement.views.Remove',
	url(r'^comment/(?P<pk>.+)/$', v.comment, name = 'advertisement-comment'),
	url(r'^reply/(?P<pk>.+)/$', v.reply, name = 'advertisement-reply'),
	
]