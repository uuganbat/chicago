# !/usr/bin/python/env
# -*- coding:utf-8 -*-

from app import Nurl


urlpatterns = [
	Nurl(r'^$') > 'app.views.Home',
	Nurl(r'^contact/$') > 'app.views.Contact',
]