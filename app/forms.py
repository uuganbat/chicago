# !/usr/bin/python/env
# -*- coding:utf-8 -*-

from django import forms


class FormMixin(object):

	def __init__(self, *args, **kwargs):
		super(FormMixin, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs['class'] = 'form-control'


class FeedBack(FormMixin, forms.Form):
	name = forms.CharField(label = u'Нэр')
	email = forms.EmailField(label = u'Имайл')
	phone = forms.IntegerField(label = u'Утас')
	feedback = forms.CharField(label = u'Санал хүсэлт', widget=forms.Textarea(attrs = {'rows': 6}))