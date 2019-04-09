from django.contrib import admin

from manager.sites import site
import models as m

admin.site.register(m.Category)
admin.site.register(m.Podcast)

site.register(m.Podcast)
