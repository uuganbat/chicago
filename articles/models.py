# !/usr/bin/python/env
# -*- coding:utf-8 -*-

import re
import uuid

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _

from redactor.fields import RedactorField


class Category(models.Model):
	category = models.CharField(max_length = 100, verbose_name = _('Category'))
	slug = models.CharField(max_length = 50, verbose_name = _('Slug'))
	icon = models.CharField(max_length = 50, verbose_name = _('Icon'))

	def __unicode__(self):
		return unicode(self.category)


class Article(models.Model):
	id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	category = models.ForeignKey(Category)
	title = models.CharField(max_length = 100)
	body = RedactorField()
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
	created_at = models.DateTimeField(auto_now_add = True)

	def image(self):
		match = re.findall(ur'<img[^>]+src="([^">]+)"', self.body)
		if len(match) > 0:
			return match[0]
		return '%s/img/ub.jpg' % settings.STATIC_URL

	def get_all_comments(self):
		return Comment.objects.filter(article = self)

	def __unicode__(self):
		return unicode(self.title)


class Views(models.Model):
	article = models.ForeignKey(Article)
	ip = models.CharField(max_length = 32)
	session = models.CharField(max_length=40, null = True)
	created = models.DateTimeField(auto_now_add = True)


class Comment(models.Model):
	article = models.ForeignKey(Article)
	text = models.TextField()
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'comment_user')
	created_at = models.DateTimeField(auto_now_add = True)

	def get_all_replys(self):
		return Reply.objects.filter(comment = self)

	def __unicode__(self):
		return unicode(self.article)


class Reply(models.Model):
	comment = models.ForeignKey(Comment)
	text = models.TextField()
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'reply_user')
	created_at = models.DateTimeField(auto_now_add = True)

	def __unicode__(self):
		return unicode(self.comment)

