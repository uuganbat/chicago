from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html

class PodcastConfig(AppConfig):
    name = 'podcast'
    verbose_name = _('Podcast')
    icon = format_html('<i class="fa fa-podcast"></i>')
