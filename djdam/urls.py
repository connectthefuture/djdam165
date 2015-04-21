#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Default urlconf for djdam """
from django.conf import settings
from django.conf.urls import include, patterns, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import os, sys

import admin_tools as admin_tools
import adminactions as adminactions
from django.conf.urls import include
## Autocomplete right before admi autodiscover
import autocomplete_light
autocomplete_light.autodiscover()

from django.contrib import admin
#admin.autodiscover()
## OVERRIDE ADMIN
#from searcher import admin_custom as admin
#admin.autodiscover()
####

def bad(request):
    """ Simulates a server error """
    1 / 0

### Generic Vendor ListView Render Below with url pattern ###
    ############################################################################################################
                      ##################  ROOT URL CONF ###########################
                      ## 1###  ALL REQUESTS TO DJANGO ROUTE FROM            #######
                      ########    Gunicorn Proxy to this URL Conf File      #######
                      ## 2###  URL patterns below Further Process Request   #######
                      ########    Continuing to Route Request to      #############
                      ########      Specific App's URL Confs          #############
                      ## 3###  App URL Confs do more Specific Processing    #######
                      #######     Using Regex, Q params to Process       ##########
                      ####          that Apps views.py and      ###################
                      ########        Render Response           ###################
    ############################################################################################################

# Tastypie API Resouce URLs
#from django.conf.urls import *
from django.conf.urls import *
from tastypie.api import Api
from searcher.api.resources import SelectedFilesResource, ProductSnapshotLiveResource, ExcelToolDataResource, ViewExcelToolDuplicateVendorStyleResource, OffshoreStatusResource, OffshoreStatusSentOnlyResource, UserResource
from searcher.api.resources import PushPhotoselectsResource, Zimages1PhotoselectsResource, PostReadyOriginalResource, ProductionRawZimagesResource
from searcher.api.resources import ProductionRawCp1DataResource, ProductionRawCp1PreSelectResource, ProductionRawCp1SelectResource
from searcher.api.resources import SupplierIngestResource, SupplierIngestImagesResource, ImageUpdateResource, LookletShotListResource


v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(SelectedFilesResource())

v1_api.register(OffshoreStatusResource())
v1_api.register(OffshoreStatusSentOnlyResource())

v1_api.register(PushPhotoselectsResource())
v1_api.register(Zimages1PhotoselectsResource())
v1_api.register(PostReadyOriginalResource())
v1_api.register(ProductionRawZimagesResource())

v1_api.register(ProductionRawCp1DataResource())
v1_api.register(ProductionRawCp1PreSelectResource())
v1_api.register(ProductionRawCp1SelectResource())

v1_api.register(ExcelToolDataResource())
v1_api.register(ViewExcelToolDuplicateVendorStyleResource())

v1_api.register(ProductSnapshotLiveResource())
v1_api.register(SupplierIngestResource())
v1_api.register(SupplierIngestImagesResource())
v1_api.register(ImageUpdateResource())
v1_api.register(LookletShotListResource())

# #viewexceltoolduplicatevendorstyle_resource = ViewExcelToolDuplicateVendorStyleResource()
# from searcher.api.resources import ProductSnapshotLiveResource
# #
# productsnapshotlive_resource = ProductSnapshotLiveResource()
#
# TASTYPIE API URLS
#
######################################################################################################
#####   Django   #####################################################################################
#####   REST Framework    ############################################################################
######################################################################################################

from django.conf.urls import patterns, url, include
from rest_framework import routers
#from accounts import views as api_views
from rest_framework.urlpatterns import format_suffix_patterns


#### REST FRAMWORK URLS Views in Accounts for now
urlpatterns = patterns('accounts.views',
    ## Image Cache Clear Update Api
    url(r'^image-update-list/$', 'image_update_list'),
    url(r'^image-update/(?P<colorstyle>[0-9]{9}).*?/$', 'image_update_detail'),
    url(r'^image-update-detail/$', 'image_update_detail'),
    url(r'^image-update/?$', 'image_update_list'),
    ## Looklet Shot List Update Api
    url(r'^looklet-shot-list-update/?$', 'looklet_shot_list_update_list'),
    url(r'^looklet-shot-list-update/(?P<photodate>\d{4}-\d+-\d{2})?/?(?P<colorstyle>\d{9})?/?$', 'looklet_shot_list_update_detail'),
    url(r'^looklet-shot-list-update-detail/$', 'looklet_shot_list_update_detail'),
)
urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]

from rest_framework.authtoken import views
urlpatterns += [
    url(r'^api-token-auth/', views.obtain_auth_token)
]

## End REST

### Tastypy URLS
urlpatterns += patterns('',
    # ...more URLconf bits here...
    # Then add:
    #(r'^api/', include(v1_api.urls)),
    (r'^api/v1/pmdata/(?P<colorstyle>\d{9})/?', include(ProductSnapshotLiveResource().urls)),
    (r'^api/v1/users/?.*?$', include(UserResource().urls)),
    (r'^api/v1/excel-tool-data/(?P<colorstyle>\d{9})/?', include(ExcelToolDataResource().urls)),
    (r'^api/v1/duplicate-vendor-style/(?P<colorstyle>\d{9})/?', include(ViewExcelToolDuplicateVendorStyleResource().urls)),
    (r'^api/v1/offshore-style/(?P<colorstyle>\d{9})/?', include(OffshoreStatusResource().urls)),
    (r'^api/v1/offshore-sent/(?P<colorstyle>\d{9})/?', include(OffshoreStatusSentOnlyResource().urls)),
    (r'^api/v1/supplier-ingest/(?P<colorstyle>\d{9})/(?P<alt>\d{1,5})/?', include(SupplierIngestResource().urls)),
    (r'^api/v1/supplier-ingest-images/(?P<colorstyle>\d{9})?([_a-z0-9]{2,7})?/?$', include(SupplierIngestImagesResource().urls)),
    (r'^api/v1/supplier-ingest-images/(?P<colorstyle>\d{9})/(?P<alt>\d)/?$', include(SupplierIngestImagesResource().urls)),
    #(r'^api/v1/supplier-ingest-images/(?P<colorstyle>\d{9})(?P<alt>[_a-z0-9]{2,7})?/?', include(SupplierIngestImagesResource().urls)),
    (r'^api/v1/image-update/(?P<colorstyle>\d{9})/?$', include(ImageUpdateResource().urls)),
    #(r'^api/v1/looklet-shot-list/?(?P<photo_date>\d{4}-\d+-\d{2})?/?(?P<colorstyle>\d{9})?/?$', include(LookletShotListResource().urls)),
    (r'^api/v1/looklet-shot-list/?.*?$', include(LookletShotListResource().urls)),
    (r'^api/', include(v1_api.urls)),
)

from django.conf.urls import include, url
#from djdam.admin import *

# urlpatterns += patterns('',
#     (r'^admin/', include(admin.urls)),
# )
from django.contrib.auth import views as auth_views


urlpatterns += patterns('',
                       ## Admin -> dj admin tools actions and other admin config routing,
                       #  must load prior to django Admin loading
                       ## (r'^api/', include(v1_api.urls)),
                       url(r'^admin_tools/', include('admin_tools.urls')),
                       url(r'^adminactions/', include('adminactions.urls')),
                       # Uncomment the next line to enable the admin:
                       ## (r'^grappelli/', include('grappelli.urls')),  # grappelli Admin URLS
                       url(r'^admin/', include(admin.site.urls)),
                       #url(r'^admin/', include(admin.site.urls)),
                       #url(r'^admin/$', admin.site.admin_view(admin.site.index)),
                       ## Uncomment the admin/doc line below to enable admin
                       # documentation:
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       ## Reset passwords
                       url(r'^admin/password_reset/$', auth_views.password_reset, name='admin_password_reset'),
                       url(r'^admin/password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
                       url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', auth_views.password_reset_confirm,
                           name='password_reset_confirm'),
                       url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

                       ## End admin configs
                       #url(r'^', include('debug_toolbar_user_panel.urls')),


                       ### Load Base Site urls incl HomePage
                       url(r'', include('base.urls')),

                       ### Load Other Apps Url Confs
                       url(r'^searcher/', include('searcher.urls')),
                       url(r'^imgadjust/', include('imgadjust.urls')),
                       ## New Url Confs
                       url(r'^assets/', include('digassets.urls')),
                       url(r'^ajaxsearch/', include('ajaxsearch.urls')),
                       url(r'^uploader/', include('uploader.urls')),
                       #url(r'^ajax/', include('searcher.urls')),
                       #    url(r'^images/', include('images.urls')),
                       #    url(r'^photo/', include('photo.urls')),
                       ## Include autocompleter
                       url(r'^autocomplete/', include('autocomplete_light.urls')),
                       # # Debug tool bar html tidy panel
                       # url(r'^', include('debug_toolbar_htmltidy.urls')),

                       ### Direct Bad requests to Someting
                       url(r'^bad/$', bad),
                       #url(r'^vendors/$', list_detail.object_list, vendor_info),
                       )


#urlpatterns += patterns('',
#    (r'^ajax-upload/', include('ajax_upload.urls')),
#    (r'^ajax-upload/', include('ajax_upload.urls')),
#)

urlpatterns += patterns('',
    url(r'^accounts/', include('accounts.urls')),
)


if settings.DEBUG and settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


print "primary urls.py END"
# In DEBUG mode, serve media files through Django.
# if settings.DEBUG:
#     urlpatterns += staticfiles_urlpatterns()
# Remove leading and trailing slashes so the regex matches.
#     media_url = settings.MEDIA_URL.lstrip('/').rstrip('/')
#     urlpatterns += patterns('',
#         (r'^%s/(?P<path>.*)$' % media_url, 'django.views.static.serve',
#          {'document_root': settings.MEDIA_ROOT}),
#     )


from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns += patterns('',
                        # (r'^searcher/', include('searcher.urls')),
                        # (r'^imgadjust/', include('imgadjust.urls')),
                        (r'^$', RedirectView.as_view(url='/searcher/list/')), # Just for ease of use.
                        ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
