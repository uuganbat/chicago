# !/usr/bin/python/env
# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib.auth import views as auth_views


import views as v
import forms as f
from app import Nurl

urlpatterns = [

	url(r'^login/$', auth_views.login, {
		'template_name' : 'authenticate/ui/login.html',
		'authentication_form' : f.Login,
		}, name = 'login'),
	url(r'^logout/$', auth_views.logout, name = 'logout'),
    url(r'^change-password/$', auth_views.password_change, {
        'template_name' : 'authenticate/ui/change_password.html',
        'password_change_form': f.ChangePassword,
        'post_change_redirect' : '/',}, name = 'change-password'),
    
    url(r'^password/reset/$', auth_views.password_reset, {
        'template_name' : 'authenticate/ui/password_reset.html',
        'password_reset_form': f.PasswordReset,
        }, name="password_reset"),
    
    url(r'^password/reset/done/$', auth_views.password_reset_done, {
        #'template_name' : 'password/password_reset_done.html'
        }, name="password_reset_done"),

    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, {
            'template_name' : 'authenticate/ui/password_reset_confirm.html',
            'set_password_form': f.SetPassword,
            }, name="password_reset_confirm"),

    url(r'^password/reset/complete/$', auth_views.password_reset_complete, {
        #'template_name' : 'authenticate/ui/password_reset_complete.html'
        }, name="password_reset_complete"),
    
    url(r'^settings/$', v.settings, name='settings'),
    url(r'^settings/password/$', v.password, name='password'),
    Nurl(r'^profile/(?P<pk>.+)/$') > 'authenticate.views.Profile',
    Nurl(r'^edit/(?P<pk>.+)/$') > 'authenticate.views.Edit',
    Nurl(r'^register/$') > 'authenticate.views.Register',
    Nurl(r'^active/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$') > 'authenticate.views.Active',

]