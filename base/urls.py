#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""urlconf for the base application"""

from django.conf.urls import url, patterns, include
from base import views


urlpatterns = patterns('base.views',
                       url(r'^$', 'home', name='jbhome'),
                       ##    (r'^adminactions/', include(include(adminactions.urls))),
                       url(r'^bootstrapshell/$', 'bootstrapshell', name='bootstrapshell'),
                       url(r'^bootstrap3shell/$', 'bootstrap3shell', name='bootstrap3shell'),
                       url(r'^testhome/?$', 'testhome', name='jbtesthome'),
                       url(r'^testjsonform/?.*?$', 'testjsonform', name='testjsonform'),

)

urlpatterns += patterns('searcher.views',
                       url(r'^selected_index/?.*?$','selected_index',  name='selected_index'),
)
#
#urlpatterns += patterns('',
#                        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
#                         {'document_root': MEDIA_ROOT}),
#)

urlpatterns += patterns('searcher.tables',url(r'^suppliers/?$','suppliers'))

urlpatterns += patterns('searcher.tables',
    url(r'^suppliers/(?P<vendor_name>\w+)/?$', 'supplier_detail'),
    url(r'^suppliers/brand/(?P<vendor_brand>\w+)/?$', 'supplier_detail'),
    url(r'^suppliers/filter/?.*?$', 'supplier_filter'),

)

from searcher.tables import FilteredSingleTableView,SupplierIngestTable
from searcher.models import SupplierIngest

urlpatterns += patterns('searcher.tables',url(r'^filtered/.*?$', FilteredSingleTableView.as_view(
                                                table_class = SupplierIngestTable,
                                                model= SupplierIngest,
                                                template_name ='tables/supplier-ingest-detail.html',
                                                table_pagination={ "per_page":50 } ))
)
                                               # name='filtered_single_table_view')