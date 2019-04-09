

from django.contrib.admin.options import ModelAdmin


class ModelManager(ModelAdmin):


	'''def get_urls(self):
        from django.conf.urls import url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name

        urlpatterns = [
            url(r'^$', wrap(self.changelist_view), name='%s_%s_changelist' % info),
            url(r'^add/$', wrap(self.add_view), name='%s_%s_add' % info),
            url(r'^(.+)/history/$', wrap(self.history_view), name='%s_%s_history' % info),
            url(r'^(.+)/delete/$', wrap(self.delete_view), name='%s_%s_delete' % info),
            url(r'^(.+)/change/$', wrap(self.change_view), name='%s_%s_change' % info),
            # For backwards compatibility (was the change url before 1.9)
            url(r'^(.+)/$', wrap(RedirectView.as_view(
                pattern_name='%s:%s_%s_change' % ((self.admin_site.name,) + info)
            ))),
        ]
        return urlpatterns'''