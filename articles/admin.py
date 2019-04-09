from django.contrib import admin

import models as m
from manager.sites import site

admin.site.register(m.Category)
admin.site.register(m.Article)
admin.site.register(m.Comment)
admin.site.register(m.Reply)
admin.site.register(m.Views)


#site.register(m.Category)
site.register(m.Article)
#site.register(m.Comment)
#site.register(m.Reply)