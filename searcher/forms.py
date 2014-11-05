#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################
__author__ = 'johnb'
import django.forms as forms
from django.forms import Form
from django.forms import ModelChoiceField
from django.forms import ChoiceField

# forms.py
import floppyforms as forms
from __builtin__ import open


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
from searcher.models import Product


class NewListingForm(forms.Form):
    name = forms.CharField(required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)
    product = forms.ModelChoiceField(queryset=Product.objects.all(),
                                  empty_label="(Nothing)")

###############################################################
## custom storage images

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
from searcher.models import Asset

class UploadAssetForm(forms.Form):
#    file_path = forms.ImageField(required=True)
    file_path = forms.FileField(required=True)


    def create(self, file):
        asset = Asset()
        asset.save_asset_file(file.name, file, save=True)
        return asset

# # apps/searcher/views.py
# from searcher.forms import UploadAssetForm

# def upload(request):
#     form = UploadAssetForm(request.POST, request.FILES)

#     if not form.is_valid():
#         # Return some error
#         pass

#     # Return success


################
from django import forms
from searcher.models import SelectedFiles


class ImportCropUploadForm(forms.Form):
#    file_path = forms.ImageField(required=True)
    file_path = forms.FileField(required=True)

    def create(self, file_path):
        selected_file = SelectedFiles()
        selected_file.save_selected_file_path(file_path.name, file_path, save=True)
        return selected_file

# # apps/searcher/views.py
# from searcher.forms import ImportCropUploadForm

# def upload(request):
#     form = ImportCropUploadForm(request.POST, request.FILES)

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

from searcher.models import *

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


class ImagesForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ('id',
            'image_select_thumb',
            'image_select_push',
            'image_select',
            'image_outtake',
            )

class ImageUpdateForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput(), initial=1)
    colorstyle = forms.CharField(max_length=9, help_text="Please enter the Colorstyle")
    alt = forms.IntegerField()

    class Meta:
        model = ImageUpdate
        fields = ('id',
            'colorstyle',
            'alt',
            )

class MetadataBasicForm(forms.ModelForm):
    class Meta:
        model = Metadata
        fields = ('metadata_type',
            'metadata_tag',
            'metadata_value',
            'keywords',
            )

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class MetadataForm(forms.Form):

    file_path = forms.TypedChoiceField(
        label = "Select a file to upload and embed metadata",
        choices = ((1, "Select"), (0, "No")),
        coerce = lambda x: bool(int(x)),
        widget = forms.RadioSelect,
        initial = '0',
        required = True,
    )

    tag_type = forms.TypedChoiceField(
        label = "What Tag Type to Add?",
        choices = ((3, "IPTC"), (2, "XMP"), (1, "EXIF"), (0, "BFLY")),
        coerce = lambda x: bool(int(x)),
        widget = forms.RadioSelect,
        initial = '2',
        required = True,
    )

    tag_name = forms.CharField(
        label = "What Tag Name to Add?",
        max_length = 80,
        required = True,
    )

    tag_value = forms.CharField(
        label = "What Tag Value to Add?",
        max_length = 80,
        required = True,
    )

    keywords = forms.CharField(
        label = "Additional notes or keywords",
        required = False,
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-metadatForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_embed_metadata'

        self.helper.add_input(Submit('submit', 'Submit'))
        super(MetadataForm, self).__init__(*args, **kwargs)


class ImageNotesForm(forms.Form):
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

from django.http.response import HttpResponseRedirect
from django.views.generic.base import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext

def create(request):
    form1 = ImagesForm(request.POST, request.FILES or None)
    form2 = AlbumForm(request.POST or None)
    if form2.is_valid() and form1.is_valid():
        image = form1.save(commit=False)
        image.product = Product.objects.get(pk=3)
        image.save()
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
## LocalImageURL
######################## Form and Formset Factory
import django.forms
from searcher.models import LocalImageURL
from django.forms import ModelForm, Form
from django.forms.models import modelformset_factory
class LocalImageURLForm(forms.ModelForm):
    class Meta:
        model = LocalImageURL

LocalImageURLFormSet = modelformset_factory(LocalImageURL, max_num=7) ##fields=('name', 'title'))

###############################################################
# Message Crispy Form Example
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class MessageForm(forms.Form):
    text_input = forms.CharField()

    textarea = forms.CharField(
        widget = forms.Textarea(),
    )

    radio_buttons = forms.ChoiceField(
        choices = (
            ('option_one', "Option one is this and that be sure to include why it's great"),
            ('option_two', "Option two can is something else and selecting it will deselect option one")
        ),
        widget = forms.RadioSelect,
        initial = 'option_two',
    )

    checkboxes = forms.MultipleChoiceField(
        choices = (
            ('option_one', "Option one is this and that be sure to include why it's great"),
            ('option_two', 'Option two can also be checked and included in form results'),
            ('option_three', 'Option three can yes, you guessed it also be checked and included in form results')
        ),
        initial = 'option_one',
        widget = forms.CheckboxSelectMultiple,
        help_text = "<strong>Note:</strong> Labels surround all the options for much larger click areas and a more usable form.",
    )

    appended_text = forms.CharField(
        help_text = "Here's more help text"
    )

    prepended_text = forms.CharField()

    prepended_text_two = forms.CharField()

    multicolon_select = forms.MultipleChoiceField(
        choices = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')),
    )

    # Uni-form
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('text_input', css_class='input-xlarge'),
        Field('textarea', rows="3", css_class='input-xlarge'),
        'radio_buttons',
        Field('checkboxes', style="background: #FAFAFA; padding: 10px;"),
        AppendedText('appended_text', '.00'),
        PrependedText('prepended_text', '<input type="checkbox" checked="checked" value="" id="" name="">', active=True),
        PrependedText('prepended_text_two', '@'),
        'multicolon_select',
        FormActions(
            Submit('save_changes', 'Save changes', css_class="btn btn-primary"),
            Submit('cancel', 'Cancel'),
        )
    )

##
#from django import forms

# class UploadFileForm(forms.Form):
#     title = forms.CharField(max_length=50)
#     file  = forms.FileField()
#     #from django.forms.models import inlineformset_factory


# from django.http import HttpResponseRedirect
# from django.shortcuts import render_to_response
# from .forms import UploadFileForm

# # Imaginary function to handle an uploaded file.
# from somewhere import handle_uploaded_file

# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             handle_uploaded_file(request.FILES['file_path'])
#             return HttpResponseRedirect('/success/url/')
#     else:
#         form = UploadFileForm()
#     return render_to_response('upload.html', {'form': form})

# def handle_uploaded_file(f):
#     with open('some/file/name.txt', 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)



# inlineformset_factory creates a Class from a parent model (Image)
## to a child model (Metadata)
#ImageMetadataFormSet = inlineformset_factory(
#    Images,
#    Metadata,
#)

##    url(r'^edit/(?P<pk>\d+)/editmetadata$', searcher.views.EditImageMetadataView.as_view(),
##        name='images-edit-metadata',),

#class EditImageMetadataView(UpdateView):

#    model = Metadata
#    template_name = 'image/image_metadata_edit.html'
#    form_class = forms.ImageMetadataFormSet

#    def get_success_url(self):

        # redirect to the Image view.
#        return self.get_object().get_absolute_url()
def readxl_outputdict(workbk=None):
    import csv,xlrd,sys
    #workbk = sys.argv[1]
    book = xlrd.open_workbook(workbk)##sys.argv[1])
    sh = book.sheet_by_index(0)

    #convWriter = csv.writer(sys.stdout,delimiter=',', dialect='excel')

    numcols=sh.ncols
    outdict = {}
    for rx in xrange(sh.nrows):
        rowdict = {}
        for cx in xrange(sh.ncols):
            rowhead = sh.cell_value(rowx=0,colx=cx)
            rowval = sh.cell_value(rowx=rx,colx=cx)
            rowdict[rowhead] = rowval
            outdict[rx] = rowdict
    return outdict


def compile_outdict_by_rowkeys(outdict):
    from collections import defaultdict
    d = defaultdict(list)
    for r in outdict.items():
        dd = defaultdict(dict)
        for val in r[1].items():
            try:
                if type(val[1]) == float:
                    value = int(val[1])#"{0:.0}".format(val[1])
                    print value
                else:
                    value = val[1]
                #print type(val[1])
                #print r[0],val[0],value
                dd[val[0]]=value
                d[r[0]] = dd
                #print dd
                #csv_write_datedOutfile(lines.encode('ascii', 'replace'))
            except AttributeError:
                pass
    return d


def handle_uploaded_excel_file(f):
    with open('/media/output.xls', 'wb+') as destination:
        for chunk in f.read():
            destination.write(chunk)
        return os.path.abspath(destination)
from django import forms
from searcher.models import Asset

# class UploadMergeList(forms.Form):
#     import os
#     #file_path = forms.ImageField(required=True)
#
#     file_path = forms.FileField(required=False)
#     styles_list = forms.Textarea()
#     f = '/home/johnb/exceloutput.xls'
#     #name = file_path
#     # def _open(self, name, mode='rbU'):
#     #     self.path = ''
#     #     return open(self.path(name), mode)
#     #
#     # #if os.path.isfile(file_path):
#     # with _open(file_path,name) as f:
#     #
#
#     buf = handle_uploaded_excel_file(f)
#     with open(buf, 'rbU') as f:
#         readdata = readxl_outputdict(workbk=f.read())
#
#     #elif styles_list:expected string or unicode, FileField instead
#     #    readdata = styles_list.split(',')[:]
#     #compiledata = compile_outdict_by_rowkeys(readdata)
#
#     def query_duplicate_vendors(readdata):
#         formated_excel_data = compile_outdict_by_rowkeys(readdata)
#         #asset.save_asset_file(file_path.name, file_path, save=True)
#         return formated_excel_data

from django import forms

class UploadFileForm(forms.Form):
    # file = forms.FileField(  # required=False,
    #                               # label='Select a file'
    #                               # ,help_text='max. 42 megabytes'
    # )
    file_path=forms.FileField(# required=False,
                              # label='Select a file'
                              # ,help_text='max. 42 megabytes'
                                )
    input_list = forms.Textarea(attrs={'size': 10, 'title': 'Input Query'}# label='Enter Old Styles'
                                # ,help_text='max. 100 colorstyles'
                                )
    output_list = forms.TextInput(# required=False,
                                  # label = 'Enter New Styles'
                                  #,help_text = 'must be ordered like Input 100 colorstyles'
                                )


#from django.forms.models import inlineformset_factory

from django import forms

class DocumentForm(forms.Form):
    docfile = forms.FileField(
    # label='Select a file'
    )

from django.forms import ModelForm
from .models import ViewExcelToolDuplicateVendorStyle
#from api.resources import ViewExcelToolDuplicateVendorStyleResource

class InputMergeChoiceForm(forms.Form):
    merge_fields = forms.ModelChoiceField(queryset=ExcelToolData.objects.all().order_by('vendor_style','color_group_id'))
    #class Meta:
     #   model = ViewExcelToolDuplicateVendorStyle


# FileUpload form class.
import datetime
class UploadForm(ModelForm):
    file = forms.FileField()
    create_dt = forms.DateField()
    #label='Select a file'
    class Meta:
        model = File
        exclude = ('create_dt',)

        #modelformset_factory(File,
        #                     exclude=('file_path',
        #                              'file')
        #)
        #fields = ('id',
                  #'file_path',
                  #'file_name',
                  #'file',
                  #'ext',
        #)

# -*- coding: utf-8 -*-
from django import forms
from searcher.widgets import SplitJSONWidget


class testJSONForm(forms.Form):
    attrs = {'class': 'navbar-form', 'size': '40'}
    data = forms.CharField(widget=SplitJSONWidget(attrs=attrs, debug=True))



from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import TabHolder, Tab
from searcher.models import SupplierIngest, SupplierIngestImages, ProductSnapshotLive


class SupplierIngestModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SupplierIngestModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id     = 'id-supplierIngestForm'
        self.helper.form_method = 'post'
        self.helper.form_action = 'manage_supplier_ingest'
        self.helper.form_class  = 'form-vertical'
        self.helper.label_class = 'control-label'
        self.helper.field_class = 'col-md-4'
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                'Detail',
                Field('colorstyle', css_class='active'),
                'po_number',
                Div('vendor_name',
                    Field('vendor_brand', css_class='btn btn-success'),
                    'vendor_style',
                    'modified_dt')
                ),
                Tab(
                'Image Info',
                'image_url',
                'get_http_status_code',
                'vendor_image',
                'bfly_image',
                'version'
                ),
                Tab(
                'Status',
                'bfly_product_path',
                'production_complete_dt',
                'image_ready_dt',
                'copy_ready_dt',
                'start_dt'
                )
            ),
            Submit('submit', 'Submit'),
        )

    class Meta:
        model = SupplierIngest


class SupplierIngestImagesModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SupplierIngestImagesModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id     = 'id-supplierIngestImagesForm'
        self.helper.form_method = 'post'
        self.helper.form_action = 'manage_supplier_ingest_images'
        self.helper.form_class  = 'form-horizontal'
        self.helper.label_class = 'control-label'
        self.helper.field_class = 'col-lg-2'
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                'Details',
                'colorstyle',
                'alt',
                'bfly_product_path',
                'po_number',
                'modified_dt'
                ),
                Tab(
                'Vendor Images',
                'vendor_name',
                'vendor_brand',
                'vendor_style',
                'vendor_image',
                'bfly_image'
                ),
                Tab(
                'Bluefly Images',
                'file_name',
                'version',
                'bfly_local_src',
                'bfly_zoom_src',
                'bfly_zoom_site',
                'bfly_list_site',
                'bfly_pdp_site'
                )
            ),
            Submit('submit', 'Submit'),
        )


    class Meta:
        model = SupplierIngestImages


class ProductSnapshotLiveModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductSnapshotLiveModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id     = 'id-productSnapshotLiveModelForm'
        self.helper.form_method = 'post'
        self.helper.form_action = 'manage_product_snapshot_live'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'control-label'
        self.helper.field_class = 'col-lg-2'
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                'Style Info',
                'colorstyle',
                'brand',
                'color',
                'admin_image'
                ),
                Tab(
                'Vendor Info',
                'po_number',
                'po_type',
                'vendor_style',
                'track_number',
                'track_dt'
                ),
                Tab(
                'Samples',
                'sample_id',
                'sample_status',
                'sample_location',
                'status_dt',
                'track_number',
                'track_dt'
                ),
                Tab(
                'Status',
                'production_complete_dt',
                'image_ready_dt',
                'copy_ready_dt',
                'start_dt'
                )
            )
        )
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = ProductSnapshotLive


class SupplierImagesModelForm(forms.ModelForm):
    class Meta:
        model = SupplierIngestImages

    def __init__(self, *args, **kwargs):
        super(SupplierImagesModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_action = 'manage_supplier_images'
        #self.helper.form_tag = False
        #self.helper.disable_csrf = True
        self.helper.layout = Layout(
            'colorstyle',
            'alt',
            'vendor_image',
            HTML("""{% if formset.vendor_image.value %}<img class="img-responsive" src="{{ formset.vendor_image.value }}">{% endif %}""", ),
            'bfly_image',
            HTML("""{% if formset.bfly_image.value %}<img class="img-responsive" src="{{ formset.bfly_image.value }}">{% endif %}""", ),
            Submit('submit', 'Submit'),
        )