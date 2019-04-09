# !/usr/bin/python/env
# -*- coding:utf-8 -*-

from app import Nurl

urlpatterns = [
	Nurl(r'^$') > 'podcast.views.List',
	Nurl(r'^c/(?P<slug>.+)$') > 'podcast.views.List'
]