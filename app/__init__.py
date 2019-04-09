# !/usr/bin/python/env
# -*- coding:utf-8 -*-

import re
import threading
from importlib import import_module

from django.conf.urls import url
from django.core.mail import EmailMessage
from django.conf import settings


class NiceUrl(object):
    """
    Usage:

    * NiceUrl(r'example-url')    > 'app.path.to.view',
    * NiceUrl(r'example-prefix') > include('app.path.to.urls'),

    Feature:

    - Automatic name support ::

        NiceUrl(r'example-url') > 'app.app_label.views.ExamplePage'
        equal to:
        url(r'example-url', name='app_label-example-page', ExamplePage.as_view())
    """
    def __init__(self, regex, kwargs=None, name=None, prefix=''):
        self.regex = regex
        self.kwargs = kwargs
        self.name = name
        self.prefix = prefix

    def _import_view(self, view):
        """
        :input: "path.app.views.Hello"
        :return: <function Hello.as_view()>
        """
        mod_name = view.rsplit('.', 1)[0]
        class_name = view.rsplit('.', 1)[1]
        view_class = getattr(import_module(mod_name), class_name)

        return view_class.as_view()

    def _get_name(self, view):
        """
        :input: "app.{path}.views.Hello"
        :return: "{path}-hello"
        """
        view_name = view.rsplit('.')[-1]

        app_path = view[:-len(view_name)][:-len('.views')]#[len('app.'):]
        app_path = app_path.replace('.', '-')

        # Camelcase convert
        view_name = re.sub('(.)([A-Z][a-z]+)', r'\1%s\2' % '-', view_name)
        view_name = re.sub('([a-z0-9])([A-Z])', r'\1%s\2' % '-', view_name).lower()

        return '%s%s' % (app_path, view_name)

    def __gt__(self, view):
        if not isinstance(view, basestring):
            return url(self.regex, view.as_view(), kwargs=self.kwargs, name=self.name, prefix=self.prefix)
            # raise Exception('NiceUrl only support string')

        self.name = self.name or self._get_name(view)

        # if is CBV
        if view.rsplit('.', 1)[1][0].isupper():
            # import module
            view = self._import_view(view)

        self.view = view

        return url(self.regex, self.view, kwargs=self.kwargs, name=self.name)


Nurl = NiceUrl


class EmailThread(threading.Thread):
    def __init__(self, html_content, recipient_list):
        self.recipient_list = recipient_list
        self.html_content = html_content
        threading.Thread.__init__(self)

    def run (self):
        msg = EmailMessage('no reply', self.html_content, settings.EMAIL_HOST_USER, self.recipient_list)
        msg.content_subtype = "html"
        msg.send()


def send_html_mail(html_content, recipient_list):
    EmailThread(html_content, recipient_list).start()


def convert_to_latin(string):
    chars = {
        u'а': 'a',
        u'э': 'e',
        u'и': 'i',
        u'о': 'o',
        u'у': 'u',
        u'ө': 'u',
        u'ү': 'v',
        u'я': 'ya',
        u'е': 'ye',
        u'ё': 'yo',
        u'ю': 'yu',
        u'й': 'i',
        u'ы': 'ii',
        u'б': 'b',
        u'в': 'v',
        u'г': 'g',
        u'д': 'd',
        u'ж': 'j',
        u'з': 'z',
        u'к': 'k',
        u'л': 'l',
        u'м': 'm',
        u'н': 'n',
        u'п': 'p',
        u'р': 'r',
        u'с': 's',
        u'т': 't',
        u'ф': 'p',
        u'х': 'kh',
        u'ц': 'ts',
        u'ч': 'ch',
        u'ш': 'sh',
        u'щ': 'shch',
        u'ъ': '',
        u'ь': 'i',

        u'А': 'A',
        u'Э': 'E',
        u'И': 'I',
        u'О': 'O',
        u'У': 'U',
        u'Ө': 'V',
        u'Ү': 'U',
        u'Я': 'Ya',
        u'Е': 'Ye',
        u'Ё': 'Yo',
        u'Ю': 'Yu',
        u'Й': 'I',
        u'Ы': 'Ii',
        u'Б': 'B',
        u'В': 'V',
        u'Г': 'G',
        u'Д': 'D',
        u'Ж': 'J',
        u'Э': 'Z',
        u'К': 'K',
        u'Л': 'L',
        u'М': 'M',
        u'Н': 'N',
        u'П': 'P',
        u'Р': 'R',
        u'С': 'S',
        u'Т': 'T',
        u'Ф': 'P',
        u'Х': 'Kh',
        u'Ц': 'Ts',
        u'Ч': 'Ch',
        u'Ш': 'Sh',
        u'Щ': 'Shch',
        u'Ъ': '',
        u'Ь': 'I'
        }

    result = ''
    string = string.strip()

    for ch in string:
        result += ch in chars and chars[ch] or ch
    return result
