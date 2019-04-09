#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils.module_loading import autodiscover_modules

from sites import site


def autodiscover():
    autodiscover_modules('admin', register_to=site)


default_app_config = 'manager.apps.ManagerConfig'