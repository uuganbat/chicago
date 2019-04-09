from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html


class AdvertisementConfig(AppConfig):
    name = 'advertisement'
    verbose_name = _('Advertisement')
    icon = format_html('<i class="material-icons">group</i>')
