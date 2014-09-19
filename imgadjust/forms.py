#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
import crispy_forms.helper as FormHelper
from crispy_forms import layout, bootstrap

from uploader.models import UploadedImage
from ajax_upload.widgets import AjaxClearableFileInput

from models import *

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

        self.helper = FormHelper.FormHelper()
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


###############################################################
## custom storage files

from django.core.files.storage import FileSystemStorage

class CustomStorage(FileSystemStorage):
    def _open(self, name, mode='rb'):
        return File(open(self.path(name), mode))

    def _save(self, name, content):
        # here, you should implement how the file is to be saved
        # like on other machines or something, and return the name of the file.
        # In our case, we just return the name, and disable any kind of save
        return name

def get_available_name(self, name):
    return name


###############################################################

# apps/searcher/forms.py
from django import forms
from digassets.models import Asset

class UploadAssetForm(forms.Form):
#    file_path = forms.fileField(required=True)
    file_path = forms.FileField(required=True)


    def create(self, file):
        asset = Asset()
        asset.save_asset_file(file.name, file, save=True)
        return asset

# # apps/searcher/views.py
# from digassets.forms import UploadAssetForm

# def upload(request):
#     form = UploadAssetForm(request.POST, request.FILES)

#     if not form.is_valid():
#         # Return some error
#         pass

#     # Return success

###############################################################
from django.template.defaultfilters import slugify

def upload_to(path, attribute):
    def upload_callback(instance, filename):
        return '{0}{1}/{2}'.format(path, unicode(slugify(getattr(instance, attribute))), filename)

    return upload_callback

###############################################################
## Input data forms

from models import

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('id',
                  'product_info',
                  'vendor_style',
                  'vendor_brand',
                  'vendor_name',
                  'images',
        )


class ImageSourceForm(forms.ModelForm):
    class Meta:
        model = ImageSource
        fields = ('colorstyle',
                  'source_url',
                  'supplier_ingest',
                )

class ImageTypeForm(forms.ModelForm):
    class Meta:
        model = ImageType
        fields = ('colorstyle',
                  'alt',
                )

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('id',
            'image_size',
            'image_format',
            'colorstyle',
            'source_url',
            'server_url',
            )
#
#
# class MetadataForm(forms.ModelForm):
#     class Meta:
#         model = Metadata
#         fields = ('metadata_type',
#             'metadata_tag',
#             'metadata_value',
#             'keywords',
#             )
#
#
# class NotesForm(forms.Form):
#     note_date = forms.DateField()
#     user = forms.CharField(max_length=100)
#     email = forms.EmailField(required=False, label='Your e-mail address')
#     colorstyle = forms.CharField(max_length=100)
#     subject = forms.CharField(max_length=100)
#     message = forms.CharField(widget=forms.Textarea)
#
#     def clean_message(self):
#         message = self.cleaned_data['message']
#         num_words = len(message.split())
#         if num_words < 4:
#             raise forms.ValidationError("Not enough words!")
#         return message


    # if form.is_valid():
    #     subject = form.cleaned_data['subject']
    #     message = form.cleaned_data['message']
    #     sender = form.cleaned_data['sender']
    #     cc_myself = form.cleaned_data['cc_myself']

    #     recipients = ['info@example.com']
    #     if cc_myself:
    #         recipients.append(sender)

    #     from django.core.mail import send_mail
    #     send_mail(subject, message, sender, recipients)
    #     return HttpResponseRedirect('/thanks/') # Redirect after POS


def create(request):
    form1 = ImageForm(request.POST, request.FILES or None)
    form2 = ProductForm(request.POST or None)
    if form2.is_valid() and form1.is_valid():
        file = form1.save(commit=False)
        file.product = Product.objects.get(pk=3)
        file.save()
        album = form2.save(commit=False)

        album.save()
        if 'next' in request.POST:
            next = request.POST['next']
        else:
            next = reverse('product_show')
        return HttpResponseRedirect(next)

    return render_to_response('album/create.html',
                              locals(),
                              context_instance = RequestContext(request),
                              )



###############################################################
##
## Asset
######################## Form and Formset Factory
import django.forms
from digassets.models import Asset
from django.forms import ModelForm, Form
from django.forms.models import modelformset_factory
class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset

AssetFormSet = modelformset_factory(Asset, max_num=7) ##fields=('name', 'title'))

###############################################################


#from django.forms.models import inlineformset_factory

# inlineformset_factory creates a Class from a parent model (file)
## to a child model (Metadata)
#fileMetadataFormSet = inlineformset_factory(
#    files,
#    Metadata,
#)

##    url(r'^edit/(?P<pk>\d+)/editmetadata$', searcher.views.EditfileMetadataView.as_view(),
##        name='files-edit-metadata',),

#class EditfileMetadataView(UpdateView):

#    model = Metadata
#    template_name = 'file_metadata_edit.html'
#    form_class = forms.fileMetadataFormSet

#    def get_success_url(self):

        # redirect to the file view.
#        return self.get_object().get_absolute_url()