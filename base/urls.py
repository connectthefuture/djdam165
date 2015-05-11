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
                       url(r'^ajaxexample/?.*?$', 'ajaxexample', name='ajaxexample'),
                       url(r'^ajax2/?.*?$', 'ajaxexample2', name='ajaxexample2'),
                       url(r'^mongodisplay/?(?P<colorstyle>\w+?)?$', 'mongodisplay', name='mongodisplay'),
                       url(r'^mongo_imagesobj/?(?P<objectid>\w+?)?$', 'unwind_metadata_array_duplicate', name='unwind_metadata_array_duplicate'),
                       url(r'^mongo_imagesdata/?(?P<data_src>\w+?)?$', 'unwind_metadata_array_duplicate', name='unwind_metadata_array_duplicate2'),
                       url(r'^mongojquery/?.*?$', 'mongojquery', name='mongojquery'),
                       url(r'^ajaxdatatables/?.*?$', 'ajaxdatatables', name='ajaxdatatables'),
                       url(r'^onepageappview/?.*?$', 'onepageappview', name='onepageappview'),


)

urlpatterns += patterns('searcher.views',
                       url(r'^selected_index/?.*?$','selected_index',  name='selected_index'),
)


from djdam.settings import MEDIA_ROOT
urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
    )

urlpatterns += patterns('',
                        url(r'^reloadrefresh/(?P<colorstyle>\d{7,9})$', 'reloadrefresh'),
                        )

urlpatterns += patterns('searcher.tables',
                        url(r'^suppliers/?$','suppliers'),
                        url(r'^suppliers/compare/?.*?$', 'suppliers_compare'),
                        url(r'^productdata/?.*?$', 'pmdata_view'),
)

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



#################################################################################
##  Favicon loading for Firefox and Chrome from non default /favicon.ico location
from django.http import HttpResponseRedirect
from django.views.generic import RedirectView

urlpatterns += patterns('',
    url(r'^favicon\.ico/$', RedirectView.as_view(url='/static/ico/favicon.ico') , name='favicon'),
    url(r'^favicon\.ico/$', lambda x: HttpResponseRedirect('/static/ico/favicon.ico')), #google chrome favicon fix
    # url(r'^favicon\.ico/$', lambda x: HttpResponseRedirect(settings.STATIC_URL+'ico/favicon.ico')), #google chrome favicon fix
    # url(r'^favicon.ico$', RedirectView.as_view(url='/static/ico/favicon.ico', # Just for ease of use.
    #                     settings.STATIC_URL+'ico/favicon.ico')
    )
