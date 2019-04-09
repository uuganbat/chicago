# !/usr/bin/python/env
# -*- coding: utf-8 -*-

import json

from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.template.response import TemplateResponse
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.messages.views import SuccessMessageMixin

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from django import forms

from social_django.models import UserSocialAuth

import forms as f
import models as m

from app import views as v
from advertisement import models as am


class Edit(SuccessMessageMixin, v.LoginRequired, v.UpdateView):
    model = m.Profile
    form_class = f.ProfileForm
    #fields = ['career', 'about_me', 'profile_picture', 'cover_picture']
    success_message = u'Мэдээлэл амжилттай шинэчлэгдлээ.'

    def get_form(self):
        form = super(Edit, self).get_form()
        form.fields['career'].widget.attrs['class'] = 'form-control'
        form.fields['about_me'].widget.attrs['class'] = 'form-control'    
        return form

    def get_initial(self):
        fields = super(Edit, self).get_initial()
        fields['first_name'] = self.object.user.first_name
        fields['last_name'] = self.object.user.last_name
        return fields

    def form_valid(self, form):
        obj = form.save()
        user = obj.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()
        return super(Edit, self).form_valid(form)


class Profile(v.LoginRequired, v.DetailView):
    model = m.Profile
    paginate_by = 4
    
    def get(self, request, *args, **kwargs):
        profile = self.get_object()
        if not profile.user.first_name or not profile.user.last_name or not profile.phone \
        or not profile.cover_picture or not profile.profile_picture or not profile.about_me \
        or not profile.career:
            return redirect(reverse_lazy('authenticate-edit', kwargs = {'pk' : profile.id}))



        if self.request.is_ajax():
            object_list = self.get_objects()
            paginator = Paginator(object_list, self.paginate_by)

            page = self.request.GET.get('page')

            try:
                objects = paginator.page(page)
            except PageNotAnInteger:
                objects = paginator.page(1)
            except EmptyPage:
                objects = paginator.page(paginator.num_pages)

            context = {}
            context['object_list'] = objects
            return TemplateResponse(request, 'app/ui/ads.html', context)
        return super(Profile, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        context['type'] = self.request.GET.get('type')
        object_list = self.get_objects()
        paginator = Paginator(object_list, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)

        context['object_list'] = objects
        return context

    def get_objects(self):
        types = self.request.GET.get('type')
        if types == u'my':
            return am.Advertisement.objects.filter(created_by = self.request.user)
        if types == u'saved':
            return am.Advertisement.objects.filter(savedadvertisement__user = self.request.user)
        return am.Advertisement.objects.filter(created_by = self.request.user)


class Register(SuccessMessageMixin, v.CreateView):
    model = User
    form_class = f.RegisterForm
    success_message = u'Бүртгэл амжилттай хийгдлээ, %(email)s рүү орж бүртгэлээ баталгаажуулна уу.'

    def get_success_url(self):
        return reverse_lazy('app-home')

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            email = self.object.email,
        )

    def get_form_kwargs(self):
        kwargs = super(Register, self).get_form_kwargs()
        kwargs.update({'request' : self.request})
        return kwargs


class Active(v.RedirectView):
    url = reverse_lazy('login')

    def get_redirect_url(self, *args, **kwargs):
        uid = force_text(urlsafe_base64_decode(self.kwargs['uidb64']))
        user = get_object_or_404(User, pk = uid)
        if not default_token_generator.check_token(user, kwargs['token']):
            raise Http404
        user.is_active = True
        user.save()
        messages.success(self.request, 'Бүртгэл амжилттай баталгаажлаа.')
        return super(Active, self).get_redirect_url(*args, **kwargs)


@login_required
def settings(request):
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None

    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'authenticate/ui/settings.html', {
        'github_login': github_login,
        'twitter_login': twitter_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })


@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = auth_forms.PasswordChangeForm
    else:
        PasswordForm = auth_forms.AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'authenticate/ui/password.html', {'form': form})