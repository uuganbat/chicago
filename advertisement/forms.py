# !/usr/bin/python/env

from django import forms
import models as m
from django.utils.translation import ugettext as _

from redactor.widgets import RedactorEditor
from smart_selects.widgets import ChainedSelect


class AdvertisementForm(forms.ModelForm):

	class Meta:
		model = m.Advertisement
		exclude = ['created_by']
		widgets = {
			'category' : forms.Select(attrs = {'class':'form-control'}),
			'title' : forms.TextInput(attrs = {'class':'form-control'}),
			'body' : RedactorEditor(
				allow_file_upload=False,
				allow_image_upload=False
				),
			}

	def __init__(self, *args, **kwargs):
		super(AdvertisementForm, self).__init__(*args, **kwargs)
		self.fields['category'].empty_label =  _(self.fields['category'].label)
		self.fields['sub_category'].widget.attrs['class'] = 'form-control'
		self.fields['sub_category'].empty_label =  _(self.fields['sub_category'].label)


AdvertisementFormSet = forms.inlineformset_factory(
	m.Advertisement,
	m.AdvertisementImage,
	extra = 3,
	fields = ('image',),
	max_num = 3,
	can_delete = True,
	#widgets = {
    #	'image': forms.FileInput(attrs={'class':'form-control'}),
    #	}
	)