# !/usr/bin/python/env
# -*- coding:utf-8 -*-

import re
from transliterate import translit, detect_language

from django.views import generic as g
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.template.response import TemplateResponse
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse_lazy

from advertisement import models as am
from podcast import models as pm
from articles import models as arm
from app import send_html_mail, convert_to_latin

import forms as f


class LoginRequired(object):

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(LoginRequired, self).dispatch(*args, **kwargs)


class BaseMixin(object):

	def get_template_names(self):

		if self.template_name is None:
			# class name to template file name
			cname = self.__class__.__name__
			name = re.sub('(.)([A-Z][a-z]+)', r'\1%s\2' % '_', cname)
			name = re.sub('([a-z0-9])([A-Z])', r'\1%s\2' % '_', name).lower()

			namef = re.sub('(.)([A-Z][a-z]+)', r'\1%s\2' % '/', cname)
			namef = re.sub('([a-z0-9])([A-Z])', r'\1%s\2' % '/', namef).lower()

			# get app_label
			app_path = self.__module__[:-len('.views')]
			app_path = app_path.replace('.', '/')

			# prepare template name
			self.template_names = ['%s/ui/%s.html' % (app_path, name), '%s/%s.html' % (app_path, name), '%s/ui/%s.html' % (app_path, namef), '%s/%s.html' % (app_path, namef)]
			return self.template_names
		return super(BaseMixin, self).get_template_names()

	def get_context_data(self, **kwargs):
		context = super(BaseMixin, self).get_context_data(**kwargs)
		context['ads_categorys'] = am.Category.objects.all()
		context['podcast_categorys'] = pm.Category.objects.all()
		context['article_categorys'] = arm.Category.objects.all()
		user = self.request.user
		if user.is_authenticated:
			profile = user.profile
			if not user.first_name or not user.last_name or not profile.phone \
			or not profile.cover_picture or not profile.profile_picture or not profile.about_me \
			or not profile.career:
				context['profile_update'] = True
		return context


class TemplateView(BaseMixin, g.TemplateView):
	pass


class ListView(BaseMixin, g.ListView):
	include_template = None

	def get(self, request, *args, **kwargs):
		if self.request.is_ajax():
			include_template = self.get_include_template()
			self.object_list = self.get_queryset()
			queryset = self.object_list
			page_size = self.get_paginate_by(queryset)
			if page_size:
				paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, page_size)
				context = {}
				context = {
	                'paginator': paginator,
	                'page_obj': page,
	                'is_paginated': is_paginated,
	                'object_list': queryset
	            }
				return TemplateResponse(request, include_template, context)
		return super(ListView, self).get(request, *args, **kwargs)

	def get_include_template(self):
		return self.include_template

	def get_queryset(self):
		queryset = super(ListView, self).get_queryset()
		queryset = queryset.order_by('-created_at')
		search = self.request.GET.get('search')
		slug = self.kwargs.get('slug', None)
		if search:
			if not detect_language(search):
				search_mn = translit(search, 'mn')
			else:
				search_mn = convert_to_latin(search)
			queryset = self.search(search, search_mn, queryset)
		if slug is not None:
			queryset = queryset.filter(category__slug = slug)
		return queryset

	def search(self, search, search_mn, queryset):
		return queryset.filter(
				Q(title__icontains = search_mn) | Q(title__icontains=search) |
				Q(body__icontains = search_mn) | Q(body__icontains=search)
				)


class DetailView(BaseMixin, g.DetailView):
	pass


class CreateView(BaseMixin, g.CreateView):
	pass


class UpdateView(BaseMixin, g.UpdateView):
	pass


class DeleteView(BaseMixin, g.DeleteView):
	pass


class RedirectView(BaseMixin, g.RedirectView):
	pass


class FormView(BaseMixin, g.FormView):
	pass


class Home(TemplateView):
	
	'''def get_context_data(self, **kwargs):
		context = super(Home, self).get_context_data(**kwargs)
		print self.request.session['anonymous']
		return context'''


class Contact(FormView):
	form_class = f.FeedBack

	def get_success_url(self):
		return reverse_lazy('app-contact')

	def form_valid(self, form):
		context = {}
		context['name'] = form.cleaned_data['name']
		context['email'] = form.cleaned_data['email']
		context['phone'] = form.cleaned_data['phone']
		context['feedback'] = form.cleaned_data['feedback']
		template = render_to_string('app/ui/feedback.html', context)
		send_html_mail(template, ['uuganbat@innosol.mn'])
		return super(Contact, self).form_valid(form)