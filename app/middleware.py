# !/usr/bin/python/env
# -*- coding:utf-8 -*-

from django.utils.deprecation import MiddlewareMixin


class AfterMiddleware(MiddlewareMixin):

    def process_template_response(self, request, response):
        response.context_data.update({
            'base_template': 'app/ui/base.html',
            'manager_base_template': 'manager/ui/base.html'
        })
        return response