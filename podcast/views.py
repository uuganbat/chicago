# !/usr/bin/python/env
# -*- coding:utf-8 -*-

from django.template.response import TemplateResponse
from django.db.models import Q

from app import views as v
import models as m


class List(v.ListView):
	model = m.Podcast
	paginate_by = 10
	include_template = 'podcast/ui/podcast.html'

	def search(self, search, search_mn, queryset):
		return queryset.filter(Q(title__icontains = search_mn) | Q(title__icontains=search))
