from __future__ import unicode_literals

from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig

import options
from sites import site

#from articles.models import Article


class ManagerConfig(AdminConfig):
    name = 'manager'

    #def ready(self):
        #site.register(Article)
        #print "#####################"
        #print "#####################"
        #print "#####################"
        #print "#####################"
        #print "#####################"
        #print "#####################"
        #print site._registry
