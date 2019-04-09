# !/usr/bin/python/env
# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.contrib.auth import forms as auth_forms
from django import forms
from django.core.urlresolvers import reverse

from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from app import forms as af
from app import send_html_mail

import models as m


class Login(af.FormMixin, auth_forms.AuthenticationForm):
	pass


class RegisterForm(af.FormMixin, auth_forms.UserCreationForm):

	def __init__(self, request, *args, **kwargs):
		super(RegisterForm, self).__init__(*args, **kwargs)
		self.request = request

	class Meta(auth_forms.UserCreationForm.Meta):
		fields = ("username", "email")

	def save(self, commit=True):
		user = super(RegisterForm, self).save(commit = commit)
		user.is_active = False
		user.save()

		m.Profile.objects.create(user = user)

		current_site = get_current_site(self.request)
		site_name = current_site.name
		domain = current_site.domain

		uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
		token = default_token_generator.make_token(user)
		url = reverse('authenticate-active', kwargs = {'uidb64': uidb64, 'token': token})

		link = 'http://%s%s' %(domain, url)

		c = {'link': link}
		c['username'] = user.username
		template = render_to_string('authenticate/ui/register_email.html', c)
		send_html_mail(template, [user.email])
		return user


class ChangePassword(af.FormMixin, auth_forms.PasswordChangeForm):
	pass


class PasswordReset(af.FormMixin, auth_forms.PasswordResetForm):
	pass


class SetPassword(af.FormMixin, auth_forms.SetPasswordForm):
	pass


class ProfileForm(af.FormMixin, forms.ModelForm):
	first_name = forms.CharField(label = _('first name'))
	last_name = forms.CharField(label = _('last name'))

	class Meta:
		model = m.Profile
		fields = ['career', 'about_me', 'profile_picture', 'cover_picture', 'phone']

	#def __init__(self, *args, **kwargs):
	#	super(ProfileForm, self).__init__(*args, **kwargs)
	#	self.fields['first_name'].initial = 
