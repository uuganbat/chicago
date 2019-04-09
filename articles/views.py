# !/usr/bin/python/env
# -*- coding:utf-8 -*-

import re

from django.template.response import TemplateResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect

from app import views as v
import models as m


class List(v.ListView):
	model = m.Article
	paginate_by = 10
	include_template = 'articles/ui/articles.html'

	def search(self, search, search_mn, queryset):
		return queryset.filter(Q(title__icontains = search_mn) | Q(title__icontains=search))


class Detail(v.DetailView):
	model = m.Article

	def get_context_data(self, **kwargs):
		context = super(Detail, self).get_context_data(**kwargs)
		context['comments'] = self.object.get_all_comments
		if self.request.user.is_authenticated():
			if not m.Views.objects.filter(
				article = self.object,
				ip = self.request.META['REMOTE_ADDR'],
				session = self.request.session.session_key).exists():
				m.Views.objects.create(
					article = self.object,
					ip = self.request.META['REMOTE_ADDR'],
					session = self.request.session.session_key)
		else:
			if not m.Views.objects.filter(
				article = self.object,
				ip = self.request.META['REMOTE_ADDR']).exists():
				m.Views.objects.create(
					article = self.object,
					ip = self.request.META['REMOTE_ADDR'])
		context['count'] = m.Views.objects.filter(article = self.object).count()
		return context


class Create(v.CreateView):
	model = m.Article
	fields = ('__all__')


@csrf_protect
def comment(request, pk):
	if request.POST:
		article = m.Article.objects.get(pk = pk)
		text = request.POST.get('text', None)
		m.Comment.objects.create(article = article, text = text, user = request.user)
		context = {}
		context['comments'] = m.Comment.objects.filter(article = article)
		context['object'] = article
		return TemplateResponse(request, 'articles/ui/comment.html', context)


@csrf_protect
def reply(request, pk):
	if request.POST:
		comment = m.Comment.objects.get(pk = pk)
		article = comment.article
		text = request.POST.get('text', None)
		m.Reply.objects.create(comment = comment, text = text, user = request.user)
		context = {}
		context['comments'] = m.Comment.objects.filter(article = article)
		context['object'] = article
		return TemplateResponse(request, 'articles/ui/comment.html', context)
