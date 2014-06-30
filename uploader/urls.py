#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from djdam.apps import *
## from searcher.models import ProductSnapshotLive, ProductionRawOnfigure, ProductionRawZimages
from uploader import views

from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

#from ajaxuploader.views import AjaxFileUploader

#uploader = AjaxFileUploader()
import ajaxuploader

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('uploader.views',
    #url(r'^helper/ajax-upload/$', 'uploader', name="ajax_uploader"),
    url(r'^$', 'image_list', name='image_list'),
    url(r'^images/(?P<image_id>\d*)/$', 'image_upload', name='change_image'),
    url(r'^images/add/$', 'image_upload', name='add_image'),
    url(r'^addedit/$', 'add_edit_image', name='addedit_image'),
    url(r'^addedit/(?P<uploaded_image_id>\d+)/$', 'add_edit_image', name='editadd_image'),
    #Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()

urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}, name="media_url"),
) + urlpatterns

