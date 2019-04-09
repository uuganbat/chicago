
from functools import update_wrapper

from django.apps import apps
from django.conf import settings
from django.contrib.admin import ModelAdmin, actions
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.db.models.base import ModelBase
from django.http import Http404, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import NoReverseMatch, reverse
from django.utils import six
from django.utils.text import capfirst
from django.utils.translation import ugettext as _, ugettext_lazy
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.i18n import JavaScriptCatalog

from django.contrib.admin.sites import AdminSite



class ManagerSite(AdminSite):
	index_template = 'manager/ui/dash_board.html'
	app_index_template = 'manager/ui/app_index.html'

	@property
	def urls(self):
		return self.get_urls(), 'manager', self.name

	def _build_app_dict(self, request, label=None):
		"""
		Builds the app dictionary. Takes an optional label parameters to filter
		models of a specific app.
		"""
		app_dict = {}
		if label:
			models = {
				m: m_a for m, m_a in self._registry.items()
				if m._meta.app_label == label
				}
		else:
			models = self._registry


		for model, model_admin in models.items():
			app_label = model._meta.app_label

			has_module_perms = model_admin.has_module_permission(request)
			if not has_module_perms:
				if label:
					raise PermissionDenied
				continue

			perms = model_admin.get_model_perms(request)

			# Check whether user has any perm for this module.
			# If so, add the module to the model_list.
			if True not in perms.values():
				continue

			info = (app_label, model._meta.model_name)
			model_dict = {
				'name': capfirst(model._meta.verbose_name_plural),
				'object_name': model._meta.object_name,
				'perms': perms,
				}
			if perms.get('change'):
				try:
					model_dict['admin_url'] = reverse('manager:%s_%s_changelist' % info, current_app=self.name)
				except NoReverseMatch:
					pass
			if perms.get('add'):
				try:
					model_dict['add_url'] = reverse('manager:%s_%s_add' % info, current_app=self.name)
				except NoReverseMatch:
					pass

			if app_label in app_dict:
				app_dict[app_label]['models'].append(model_dict)
			else:
				app_dict[app_label] = {
					'name': apps.get_app_config(app_label).verbose_name,
					'icon': apps.get_app_config(app_label).icon,
					'app_label': app_label,
					'app_url': reverse(
						'manager:app_list',
						kwargs={'app_label': app_label},
						current_app=self.name,
						),
					'has_module_perms': has_module_perms,
					'models': [model_dict],
					}
		if label:
			return app_dict.get(label)
		return app_dict

	def app_index(self, request, app_label, extra_context=None):
		app_lists = self.get_app_list(request)
		extra_context = {'app_lists' : app_lists}
		return super(ManagerSite, self).app_index(request, app_label, extra_context = extra_context)


site = ManagerSite(name = 'manager')