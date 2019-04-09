# !/usr/bin/python/env
# -*- coding:utf-8 -*-

from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.template.response import TemplateResponse
from django.db.models import Q

from app import views as v
from app import convert_to_latin

import models as m
import forms as f


class List(v.ListView):
	model = m.Advertisement
	paginate_by = 4
	include_template = 'advertisement/ui/ads.html'


class Detail(v.DetailView):
	model = m.Advertisement

	def get_context_data(self, **kwargs):
		context = super(Detail, self).get_context_data(**kwargs)
		obj = self.get_object()
		obj.view += 1
		obj.save()
		object_list = m.Advertisement.objects.exclude(id = obj.id).filter(
			category = obj.category,
			sub_category = obj.sub_category
			).order_by('-created_at')[:9]
		context['object_list'] = object_list
		if self.request.user.is_authenticated():
			context['is_not_saved'] = m.SavedAdvertisement.objects.filter(
				advertisement = obj,
				user = self.request.user
				).exists()

		context['max_objects'] = m.Advertisement.objects.all().order_by('-view')[:5]
		
		return context


class Create(v.LoginRequired, v.CreateView):
	model = m.Advertisement
	form_class = f.AdvertisementForm

	def get_success_url(self):
		return reverse_lazy('advertisement-detail', kwargs = {'pk': self.object.pk})

	def get(self, request, *args, **kwargs):
		self.object = None
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		advertisement_formset = f.AdvertisementFormSet()
		return self.render_to_response(self.get_context_data(form=form, advertisement_formset = advertisement_formset))

	def post(self, request, *args, **kwargs):
		self.object = None
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		advertisement_formset = f.AdvertisementFormSet(request.POST, request.FILES)
		if (form.is_valid() and advertisement_formset.is_valid()):
			return self.form_valid(form, advertisement_formset)
		else:
			return self.form_invalid(form, advertisement_formset)

	def form_valid(self, form, advertisement_formset):
		self.object = form.save(commit = False)
		self.object.created_by = self.request.user
		self.object.save()
		advertisement_formset.instance = self.object
		advertisement_formset.save()
		messages.success(self.request, u'Зар амжилттай нэмэгдлээ')
		return HttpResponseRedirect(self.get_success_url())

	def form_invalid(self, form, advertisement_formset):
		return self.render_to_response(
			self.get_context_data(form=form, advertisement_formset=advertisement_formset)
			)


class Update(v.LoginRequired, v.UpdateView):
	model = m.Advertisement
	form_class = f.AdvertisementForm

	def get_success_url(self):
		return reverse_lazy('advertisement-detail', kwargs = {'pk': self.object.pk})

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		advertisement_formset = f.AdvertisementFormSet(instance = self.object)
		print dir(advertisement_formset[0])
		return self.render_to_response(self.get_context_data(form=form, advertisement_formset = advertisement_formset))

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		advertisement_formset = f.AdvertisementFormSet(request.POST, request.FILES, instance = self.object)
		if (form.is_valid() and advertisement_formset.is_valid()):
			return self.form_valid(form, advertisement_formset)
		else:
			return self.form_invalid(form, advertisement_formset)

	def form_valid(self, form, advertisement_formset):
		form.save()
		advertisement_formset.save()
		messages.success(self.request, u'Зар амжилттай өөрчлөгдлөө.')
		return HttpResponseRedirect(self.get_success_url())

	def form_invalid(self, form, advertisement_formset):
		return self.render_to_response(
			self.get_context_data(form=form, advertisement_formset=advertisement_formset)
			)


class Save(v.LoginRequired, v.RedirectView):
	pattern_name = 'advertisement-detail'

	def get_redirect_url(self, *args, **kwargs):
		ads = m.SavedAdvertisement.objects.filter(
			advertisement_id = self.kwargs['pk'],
			user = self.request.user
			)
		if ads.exists():
			messages.warning(self.request, 'Уучлаарай, зар хадгалагдсан байна!')
		else:
			m.SavedAdvertisement.objects.create(
				advertisement_id = self.kwargs['pk'],
				user = self.request.user
				)
			messages.success(self.request, 'Зар амжилттай хадгалагдлаа.')
		return super(Save, self).get_redirect_url(*args, **kwargs)


class Remove(v.LoginRequired, v.RedirectView):
	pattern_name = 'advertisement-detail'

	def get_redirect_url(self, *args, **kwargs):
		ads = m.SavedAdvertisement.objects.get(
			advertisement_id = self.kwargs['pk'],
			user = self.request.user
			)
		ads.delete()
		messages.success(self.request, 'Зар амжилттай утслаа.')
		return super(Remove, self).get_redirect_url(*args, **kwargs)


def comment(request, pk):
	ads = m.Advertisement.objects.get(id = pk)
	comment = m.Comment.objects.create(
		advertisement = ads,
		text = request.POST.get('comment'),
		user = request.user
		)
	context = {}
	context['object'] = ads
	return TemplateResponse(request, 'advertisement/ui/comment.html', context)


def reply(request, pk):
	comment = m.Comment.objects.get(id = pk)
	reply = m.Reply.objects.create(
		comment = comment,
		text = request.POST.get('reply'),
		user = request.user
		)
	context = {}
	context['object'] = comment.advertisement
	return TemplateResponse(request, 'advertisement/ui/comment.html', context)