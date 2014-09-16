#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from uploader.models import UploadedImage
from ajax_upload.widgets import AjaxClearableFileInput


## changed from Charfiled for file_path
class UploadedImageForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        widgets = {
            'image_field': AjaxClearableFileInput
        }
        fields = ["title"]

    file_path = forms.CharField(
        max_length=255,
        widget=AjaxClearableFileInput(),
        required=False,
    )
    delete_image = forms.BooleanField(
        widget=forms.HiddenInput(),
        required=False,
    )


    def __init__(self, *args, **kwargs):
        super(UploadedImageForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        #self.helper.inputs  =
        self.helper.form_tag = False
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("UploadedImage form"),
                "title",
                layout.HTML(u"""{% load i18n %}
                    <div id="image_upload_widget">
                        <div class="preview">
                            {% if instance.image %}
                                <img src="{{ MEDIA_URL }}{{ instance.image }}" alt="" />
                            {% endif %}
                        </div>
                        <div class="uploader">
                            <noscript>
                                <p>{% trans "Please enable JavaScript to use file uploader." %}</p>
                            </noscript>
                        </div>
                        <p class="help_text" class="help-block">{% trans "Available formats are JPG, GIF, and PNG." %}</p>
                        <div class="messages"></div>
                    </div>
                """),
                "file_path",
                "delete_image",
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Save'), css_class="btn btn-warning"),
            )
        )


from django.forms.models import formset_factory
UploadedImageFormset = formset_factory(UploadedImageForm, extra = 3)
uploadedimage_formset = UploadedImageFormset()


#### dj ajax upload widget ver
from django import forms

from ajax_upload.widgets import AjaxClearableFileInput

from uploader.models import UploadedImage


class UploadedImageFormAlt(forms.ModelForm):
    class Meta:
        model = UploadedImage
        widgets = {
            'image': AjaxClearableFileInput
        }


####################
#from django.db.models import FileField
#from django.forms import forms
#from django.template.defaultfilters import filesizeformat
#from django.utils.translation import ugettext_lazy as _
#
#class ContentTypeRestrictedFileField(FileField):
#    """
#    Same as FileField, but you can specify:
#        * content_types - list containing allowed content_types. Example: ['application/pdf', 'image/jpeg']
#        * max_upload_size - a number indicating the maximum file size allowed for upload.
#            2.5MB - 2621440
#            5MB - 5242880
#            10MB - 10485760
#            20MB - 20971520
#            50MB - 5242880
#            100MB 104857600
#            250MB - 214958080
#            500MB - 429916160
#    """
#    def __init__(self, content_types=None,max_upload_size=104857600, **kwargs):
#        self.content_types = kwargs.pop('video/avi', 'video/mp4', 'video/3gp', 'video/wmp', 'video/flv', 'video/mov')
#        self.max_upload_size = max_upload_size
#
#        super(ContentTypeRestrictedFileField, self).__init__(**kwargs)
#
#
#    def clean(self, *args, **kwargs):
#        data = super(ContentTypeRestrictedFileField, self).clean(*args, **kwargs)
#
#        file = data.file
#        try:
#            content_type = file.content_type
#            if content_type in self.content_types:
#                if file._size > self.max_upload_size:
#                    raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(self.max_upload_size), filesizeformat(file._size)))
#            else:
#                raise forms.ValidationError(_('Filetype not supported.'))
#        except AttributeError:
#            pass
#
#        return data
#
#        #from south.modelsinspector import add_introspection_rules
#        #add_introspection_rules([], ["^app\.extra\.ContentTypeRestrictedFileField"])