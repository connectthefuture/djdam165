#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################

import django.forms as forms
from django.forms import Form
from django.forms import ModelChoiceField
from django.forms import ChoiceField
from digassets.models import *

# forms.py
import floppyforms as forms


class DatePicker(forms.DateInput):
    template_name = 'datepicker.html'

    class Media:
        js = (
            'js/jquery.min.js',
            'js/jquery-ui.min.js',
        )
        css = {
            'all': (
                'css/jquery-ui.css',
            )
        }


class DateForm(forms.Form):
    date = forms.DateField(widget=DatePicker)


def get_my_choices():
    # you place some logic here
    choices_list = []   
    return choices_list
 
class MyForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(MyForm, self).__init__(*args, **kwargs)
        self.fields['my_choice_field'] = forms.ChoiceField(
            choices=get_my_choices() )



########################################


class NewListingForm(forms.Form):
    name = forms.CharField(required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)
    product = forms.ModelChoiceField(queryset=Product.objects.all(), 
                                  empty_label="(Nothing)")

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

from digassets.models import *

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ('title',
            'rating',
            )


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('tag',)


class FilesForm(forms.ModelForm):
    class Meta:
        model = Files
        fields = ('id', 
            'file_select_thumb',
            'file_select_push',            
            'file_select',
            'file_outtake',
            )


class MetadataForm(forms.ModelForm):
    class Meta:
        model = Metadata
        fields = ('metadata_type', 
            'metadata_tag', 
            'metadata_value', 
            'keywords',
            )


class NotesForm(forms.Form):
    note_date = forms.DateField()
    user = forms.CharField(max_length=100)
    email = forms.EmailField(required=False, label='Your e-mail address')
    colorstyle = forms.CharField(max_length=100)
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)

    def clean_message(self):
        message = self.cleaned_data['message']
        num_words = len(message.split())
        if num_words < 4:
            raise forms.ValidationError("Not enough words!")
        return message


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
    form1 = FilesForm(request.POST, request.FILES or None)
    form2 = AlbumForm(request.POST or None)
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
