# !/usr/bin/python/env

from django.contrib import admin

from manager.sites import site
import models as m

class ImageStacked(admin.StackedInline):
	model = m.AdvertisementImage
	extra = 0


class AdvertisementAdmin(admin.ModelAdmin):
	model = m.Advertisement
	inlines = [ImageStacked]


admin.site.register(m.Category)
admin.site.register(m.SubCategory)
admin.site.register(m.Advertisement, AdvertisementAdmin)
admin.site.register(m.AdvertisementImage)
admin.site.register(m.SavedAdvertisement)
admin.site.register(m.Comment)
admin.site.register(m.Reply)


site.register(m.Advertisement, AdvertisementAdmin)
