# !/usr/bin/python/env
# -*- cofing:utf-8 -*-

import uuid

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse


class Profile(models.Model):
	id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	profile_picture = models.ImageField(verbose_name = _('Profile picture'), null = True, blank = True)
	cover_picture = models.ImageField(verbose_name = _('Cover picture'), null = True, blank = True)
	career = models.CharField(max_length = 50, verbose_name = _('Career'), null = True, blank = True)
	about_me = models.TextField(verbose_name = _('About me'), null = True, blank = True)
	phone = models.IntegerField(verbose_name = _('Phone'), null = True, blank = True)
	facebook = models.CharField(max_length = 50, verbose_name = _('Facebook'), null = True, blank = True)
	twitter = models.CharField(max_length = 50, verbose_name = _('Twitter'), null = True, blank = True)
	google = models.CharField(max_length = 50, verbose_name = _('Google'), null = True, blank = True)

	def profile_img(self):
		if self.profile_picture and hasattr(self.profile_picture, 'url'):
			return self.profile_picture.url
		return '%simg/default-avatar.png' % settings.STATIC_URL

	def cover_img(self):
		if self.cover_picture and hasattr(self.cover_picture, 'url'):
			return self.cover_picture.url
		return '%simg/bg4.jpeg' % settings.STATIC_URL

	def get_absolute_url(self):
		return reverse("authenticate-profile", kwargs={"pk": self.id})

	def __unicode__(self):
		return unicode(self.user)