from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _


class Category(models.Model):
	category = models.CharField(max_length = 100, verbose_name = _('Category'))
	slug = models.CharField(max_length = 50, verbose_name = _('Slug'))
	icon = models.CharField(max_length = 50, verbose_name = _('Icon'))

	def __unicode__(self):
		return unicode(self.category)


class Podcast(models.Model):
	category = models.ForeignKey(Category, verbose_name = _('Category'))
	title = models.CharField(max_length = 100, verbose_name = _('Title'))
	image = models.ImageField(verbose_name = _('Image'))
	audio = models.FileField(verbose_name = _('Audio'))
	url = models.URLField(verbose_name = _('Url'), null = True)
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name = _('Created_by'))
	created_at = models.DateTimeField(auto_now_add = True)

	def __unicode__(self):
		return unicode(self.title)