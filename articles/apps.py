from __future__ import unicode_literals

from django.apps import AppConfig

from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html


class ArticlesConfig(AppConfig):
    name = 'articles'
    verbose_name = _('Articles')
    icon = format_html('<i class="fa fa-newspaper-o"></i>')
