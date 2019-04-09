# !/usr/bin/python/env
# -*- coding:utf-8 -*-

import uuid

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _

from smart_selects.db_fields import ChainedForeignKey
from redactor.fields import RedactorField

from app import convert_to_latin


class Category(models.Model):
	category = models.CharField(max_length = 200, verbose_name = _('Category'))
	slug = models.CharField(max_length = 50, verbose_name = _('Slug'))
	icon = models.CharField(max_length = 50, verbose_name = _('Icon'))

	def __unicode__(self):
		return unicode(self.category)


class SubCategory(models.Model):
	category = models.ForeignKey(Category)
	sub_category = models.CharField(max_length = 200, verbose_name = _('Sub category'))

	def __unicode__(self):
		return unicode(self.sub_category)


class Advertisement(models.Model):
	id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	category = models.ForeignKey(Category)
	sub_category = ChainedForeignKey(
		SubCategory,
		chained_field = 'category',
		chained_model_field="category", 
		show_all=False, 
		auto_choose=True,
        sort=True
		)
	title = models.CharField(max_length = 70, verbose_name = _('Title'))
	body = RedactorField(verbose_name = _('Body'),
		allow_file_upload=False,
		allow_image_upload=False
		)
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
	created_at = models.DateTimeField(auto_now_add = True)
	view = models.IntegerField(default = 0, editable = False)

	def __unicode__(self):
		return unicode(self.title)


class AdvertisementImage(models.Model):
	advertisement = models.ForeignKey(Advertisement, on_delete = models.CASCADE)
	image = models.ImageField()


class SavedAdvertisement(models.Model):
	advertisement = models.ForeignKey(Advertisement)
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	created_at = models.DateTimeField(auto_now_add = True)


class Comment(models.Model):
	advertisement = models.ForeignKey(Advertisement)
	text = models.TextField()
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	created_at = models.DateTimeField(auto_now_add = True)


class Reply(models.Model):
	comment = models.ForeignKey(Comment)
	text = models.TextField()
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	created_at = models.DateTimeField(auto_now_add = True)