#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'johnb'

from django.db import models
from django.http.response import Http404

def method_splitter(request, *args, **kwargs):
    get_view = kwargs.pop('GET', None)
    post_view = kwargs.pop('POST', None)
    if request.method == 'GET' and get_view is not None:
        return get_view(request, *args, **kwargs)
    elif request.method == 'POST' and post_view is not None:
        return post_view(request, *args, **kwargs)
    raise Http404


# #Model definitions
# class Photo(models.Model):
#     name = models.CharField()
#     image = models.ImageField(upload_to=('uploads/' + 'name'))
#
# class Screenshot(models.Model):
#     title = models.CharField()
#     image = models.ImageField(upload_to=upload_to('uploads/', 'title'))
#
# ################<#<
#
#
# import os
# from django.db import models
#
# def get_image_path(instance, filename):
#     return os.path.join('photos', str(instance.id), filename)
#
# class Photo(models.Model):
#     image = models.ImageField(upload_to=get_image_path)



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
from models import Asset

class UploadAssetForm(forms.Form):
#    file_path = forms.ImageField(required=True)
    file_path = forms.FileField(required=True)


    def create(self, file):
        asset = Asset()
        asset.save_asset_file(file.name, file, save=True)
        return asset

# apps/searcher/views.py
from forms import UploadAssetForm

def upload(request):
    form = UploadAssetForm(request.POST, request.FILES)

    if not form.is_valid():
        # Return some error
        pass

    # Return success

###############################################################
from django.template.defaultfilters import slugify


def upload_to(path, attribute):
    def upload_callback(instance, filename):
        return '{0}{1}/{2}'.format(path, unicode(slugify(getattr(instance, attribute))), filename)

    return upload_callback

#####################

import datetime

from django.db.models.query import QuerySet, ValuesQuerySet
from django.http import HttpResponse


class ExcelResponse(HttpResponse):

    def __init__(self, data, output_name='excel_data', headers=None,
                 force_csv=False, encoding='utf8', font=''):

        # Make sure we've got the right type of data to work with
        valid_data = False
        if isinstance(data, ValuesQuerySet):
            data = list(data)
        elif isinstance(data, QuerySet):
            data = list(data.values())
        if hasattr(data, '__getitem__'):
            if isinstance(data[0], dict):
                if headers is None:
                    headers = data[0].keys()
                data = [[row[col] for col in headers] for row in data]
                data.insert(0, headers)
            if hasattr(data[0], '__getitem__'):
                valid_data = True
        assert valid_data is True, "ExcelResponse requires a sequence of sequences"

        import StringIO
        output = StringIO.StringIO()
        # Excel has a limit on number of rows; if we have more than that, make a csv
        use_xls = False
        if len(data) <= 65536 and force_csv is not True:
            try:
                import xlwt
            except ImportError:
                # xlwt doesn't exist; fall back to csv
                pass
            else:
                use_xls = True
        if use_xls:
            book = xlwt.Workbook(encoding=encoding)
            sheet = book.add_sheet('Sheet 1')
            styles = {'datetime': xlwt.easyxf(num_format_str='yyyy-mm-dd hh:mm:ss'),
                      'date': xlwt.easyxf(num_format_str='yyyy-mm-dd'),
                      'time': xlwt.easyxf(num_format_str='hh:mm:ss'),
                      'font': xlwt.easyxf('%s %s' % (u'font:', font)),
                      'default': xlwt.Style.default_style}

            for rowx, row in enumerate(data):
                for colx, value in enumerate(row):
                    if isinstance(value, datetime.datetime):
                        cell_style = styles['datetime']
                    elif isinstance(value, datetime.date):
                        cell_style = styles['date']
                    elif isinstance(value, datetime.time):
                        cell_style = styles['time']
                    elif font:
                        cell_style = styles['font']
                    else:
                        cell_style = styles['default']
                    sheet.write(rowx, colx, value, style=cell_style)
            book.save(output)
            mimetype = 'application/vnd.ms-excel'
            file_ext = 'xls'
        else:
            for row in data:
                out_row = []
                for value in row:
                    if not isinstance(value, basestring):
                        value = unicode(value)
                    value = value.encode(encoding)
                    out_row.append(value.replace('"', '""'))
                output.write('"%s"\n' %
                             '","'.join(out_row))
            mimetype = 'text/csv'
            file_ext = 'csv'
        output.seek(0)
        super(ExcelResponse, self).__init__(content=output.getvalue(),
                                            mimetype=mimetype)
        self['Content-Disposition'] = 'attachment;filename="%s.%s"' % \
            (output_name.replace('"', '\"'), file_ext)


# apps/searcher/forms.py
from django import forms
from models import File

class UploadExcelFileForm(forms.Form):
#    file_path = forms.ImageField(required=True)
    file_path = forms.FileField(required=True)

    def create(self, file):
        file = File()
        file.save(file, file.name)
        return file

# <!-- Button trigger modal -->
# <button class="btn btn-primary btn-lg" data-toggle="modal" data-target="#myModal"> Launch demo modal </button>
#
# <!-- Modal -->
#  <div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
#  		<div class="modal-dialog">
#  				<div class="modal-content">
#
#  						<div class="modal-header">
#
# <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
#
# <h4 class="modal-title" id="myModalLabel">Modal title</h4>
# 							</div>
#
# 							<div class="modal-body"> ... </div>
# <div class="modal-footer"> <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
# <button type="button" class="btn btn-primary">Save changes</button>
# </div>
#
# 					</div>
# <!-- /.modal-content -->
#
# 			</div>
# <!-- /.modal-dialog -->
#
# 		</div>
# <!-- /.modal -->
#
# ##And the jquery ajax to get the form fields and submit it..
# 	{%  block javascript %}
#
# 	$('#myFormSubmit').click(function(e){
#       e.preventDefault();
#       alert($('#myField').val());
#       /*
#       $.post('http://path/to/post',
#          $('#myForm').serialize(),
#          function(data, status, xhr){
#            // do something here with response;
#          });
#       */
# });
#
# {% endblock %}
#
#
import __builtin__, json,yaml,re
def json_file_parse(filename):
    data = []
    with __builtin__.open(filename, 'r') as jsonfile:
        for line in jsonfile:
            try:
                line = line.lstrip()
                data.append(json.dumps(line))
            except IOError:
                print line
                pass
    return data

json_data = json.load(__builtin__.open(filename))


d = {}
for pair in json_file_parse(filename)[1:-1].split(','):
    (k,v) = pair.split(':')
    v = v.strip()
    if v == "true":
        v = "True"
    try:
        v = ast.literal_eval(v)
    except:
        print "Couldn't eval " + v
    d[k] = v

import codecs
data = []
with codecs.open(filename,'rU','utf-8') as f:
    for line in f:
        try:
            data.append(json.load(line))
        except:
            pass
# def json_datetime_handler(obj):
#     if hasattr(obj, 'isoformat'):
#         return obj.isoformat()
#     elif isinstance(obj, ...):
#         return ...
#     else:
#         raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))

#dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime) else json.JSONEncoder().default(obj)
# {% if items %}
# <tr>
# {% for item in items %}
#      <td>{{item.name}},{{item.size}}</td>
#      {% if forloop.counter|divisibleby:2 %}
#      </tr>
#      <tr>
#      {% endif %}
# {% endfor %}
# </tr>
# {% endif %}
