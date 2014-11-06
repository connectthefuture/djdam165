#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'johnb'

from django.conf.urls import patterns, include, url

# from apps import *
## from searcher.models import ProductSnapshotLive, ProductionRawOnfigure, ProductionRawZimages
from searcher import views


# info_dict = {
#     'queryset': ProductSnapshotLive.objects.all()
# }


urlpatterns = patterns('searcher.views',
                      ### url(r'^$', 'search', name='search2'),
                      ### (r'^(\d+)/$', 'album'),
                      ### (r'^(\d+)/(full|thumbnails|edit)/$', 'album'),
                      ### (r'^select/$', 'add'),
                      ### (r'^reject/$', 'remove'),
                      ### (r'^update/$', 'update'),
                      ### (r'^(?P<q>\d+)/$', 'search_colorstyle'),

                      (r'^find/(\d{5,9})/$', 'search_colorstyle'),
                      url(r'^findall/(?P<colorstyle>\d{5,9})/$', 'get_all_images_colorstyle', name='getall_colorstyle'),
                      url(r'^findall/outtakes/?$', 'get_all_images_outtakes', name='get_all_images_outtakes'),
                      #url(r'^findall/outtakes/(?P<pkey>\d+)/?$', 'get_all_images_outtakes', name='get_all_images_outtakes'),
                      (r'^findall/?$', 'get_all_images_colorstyle'),
                      # (r'^findall/?(colorstyle=\d{5,9})/$', 'get_all_images_colorstyle'),

                      ## (r'^(\d{5,9})/$', 'search_colorstyle'),
                      ## if above isnt true, ie 9 digit style num, then brand search is next on basic search
                      url(r'^find/(\w+)/$', 'get_all_images_colorstyle', name='getall_brand'), ## name='brandsearch'),
                      url(r'^find/(?P<startdate>\d{4}-\d{2}-\d{2})/$', 'get_all_images_colorstyle', name='getall_photo_date'),
                      #(r'^find/(?P<startdate>\d{4}-\d{2}-\d{2})/?(?P<enddate>\d{4}-\d{2}-\d{2})?/$', 'search_photo_date'),
                      (r'^find/(?P<keyword>\w+)/$', 'search_keyword'),

                      ## (r'^image/(\d+)/$', 'image'),
                      ## (r'^upload/(\w+)/$', 'upload'),
                      ## (r'^(?P<q>\d{5,9})/', 'main'),
                      ## (r'^(?:<q>\w*)/(?P<startdate>\d{4}-\d{2}-\d{2})/?(?P<enddate>\d{4}-\d{2}-\d{2})?/$', 'search_photo_date'),
                      ## (r'^(?P<q>\w+)/?(?P<brandsearch>on)/$', 'search_brand'), ## name='brandsearch'),
                      ## (r'^(\w+)/$', 'search_brand'), ## name='brandsearch'),
                      ## (r'^(?P<q>\w+)/?(?P<keyword>\w+)/$', 'search_keyword'),
                      ## (r'^(?P<userid>\d+)/listalbums/$', 'list_users_albums'),
                      ## (r'^(?P<userid>\d+)/?(?P<albumid>\d+)$', 'search_users_albums_byalbum'),
                      ## (r'^(?P<q>\d+)/?(?P<userid>\w+)/$', 'search_users_albums_bycolorstyle'),
                      (r'^yesterday-fashion-selects/$', 'yesterday_fashion_selects'),
                      (r'^yesterday-fashion-outtakes/$', 'yesterday_fashion_outtakes'),
                      (r'^yesterday-still-selects/$', 'yesterday_still_selects'),
                      (r'^weeks-fashion-selects/$', 'weeks_fashion_selects'),
                      (r'^weeks-fashion-outtakes/$', 'weeks_fashion_outtakes'),
                      (r'^weeks-still-selects/$', 'weeks_still_selects'),
                      (r'^lastweeks-fashion-selects/$', 'lastweeks_fashion_selects'),
                      (r'^lastweeks-fashion-outtakes/$', 'lastweeks_fashion_outtakes'),
                      (r'^lastweeks-still-selects/$', 'lastweeks_still_selects'),
                      (r'^excel/input/$', 'input_merge_list'), #, name='input_merge_list'),
                      (r'^excel/import/$', 'import_excel_file'),
                      #(r'^excel/upload/$', 'upload_file'),
                      (r'^excel/download/$', 'download_merge_file'),
                      (r'^excel/export/$', 'export_excel_file'),
                      (r'^excel/output/$', 'output_excel_table'),
                      (r'^ajax/search_form/$', 'ajax_return_search'),
                      (r'^ajax/colorstyle/$', 'ajax_colorstyle_search'), #, name='ajax_colorstyle_search'),
                      (r'^manage/local-image-urls/.*/(\d{5,9})_(\d)_?(\d{1,4})?\.(\w+)/$', 'manage_local_image_urls'),
                      (r'^manage/products/(\d{5,9})/$', 'manage_products'),

                      url(r'^manage/supplier-ingest/$', 'manage_supplier_ingest', name='manage_supplier_base'),
                      #url(r'^manage/supplier-ingest/(?P<colorstyle>\d{5,9})/?$', 'manage_supplier_ingest', name='manage_supplier_colorstyle'),
                      url(r'^manage/supplier-images/?$', 'manage_supplier_images', name='manage_supplier_images_base'),
                      #url(r'^manage/supplier-images/(?P<colorstyle>\d{5,9})/?$', 'manage_supplier_images', name='manage_supplier_images_colorstyle'),

                      ## (r'^manage/images/(\d{5,9})/(\d)?/(d\{1,4})?/$', 'manage_images'),
                      # (r'^manage/metadata/(\d{5,9})/$', 'manage_metadata'),
                      # (r'^manage/albums/$', 'manage_albums'), #_list_users'),
                      ## (r'^manage/tags/$', 'manage_tags'),
                      ## (r'^manage/selects/$', 'manage_selects'),
                      ## (r'^manage/products/$', 'manage_products'),
                      url(r'^imagenotes_add/(?P<pkey>\d+).*?$', 'imagenotes_add', name='imagenotes_add'),
                      (r'^index/$', 'index'),
                      )


## Markselected View
urlpatterns += patterns('searcher.views',
                      ##(r'^mark-selected/(?P<colorstyle>\d{5,9})/?(?P<alt>\d{1})?/?(?P<shot_number>\d{3,4})?/$', 'mark_selected'),
                      #url(r'^mark-selected/(?P<pkey>\d+).*?$', 'mark_selected', name='mark_selected'),
                      url(r'^mark-selected/\d+/.*?$', 'mark_selected', name='mark_selected'),
                      url(r'^mark-removed/\d*?/?.*?$', 'mark_removed', name='mark_removed'),
                      #url(r'selected_index/\d+/.*?$', 'searcher.views.selected_index', name='selected_index'),
                      #(r'^mark-selected/?(\d{5,9})/?(\d{1})?/?(\d{3,4})?/$', 'mark_selected'),
                      )

## Generic List View
urlpatterns += patterns('searcher.views',
                      url(r'^upload/preview/(?P<pkey>\d+).*?$', 'upload_crop_preview', name='upload_crop_preview'),
                      url(r'^upload/crop/(?P<pkey>\d+).*?$', 'upload_and_crop', name='upload_and_crop'),
                      url(r'^upload/crop/import/?', 'upload_import_crop', name='upload_import_crop'),
  )

## Generic List View
# urlpatterns += patterns('searcher.views',

#   )

## Generic List View
# from django.conf.urls import defaults
# from searcher import models, views

# urlpatterns += patterns('',
#     (r'^brands/$', views.object_list, {'model': models.Brand}),
#     (r'^images/entries/$', views.object_list, {'model': models.Images}),
# )


# info_dict = {
#     'queryset': ProductSnapshotLive.objects.all()
# }

######### Generates a Generic List View of the Product Model
# from django.views.generic import list, detail
# from searcher.models import Product
#
# product_info = {
#     'queryset': Product.objects.all(),
#     'template_name': 'listing/product_list_page.html',
#     }
#
#
# urlpatterns += patterns('',
#     (r'^i/$', views.object_list, product_info),
#     )
#


# ## Edit/Show Metadata on single images
urlpatterns += patterns('searcher.views',
                    url(r'^metadata/edit/(\d+)/?$', 'metadata_edit_file'),
                    url(r'^metadata/edit/\d+/.*?$', 'metadata_edit_file', name='metadata_edit_file'),
                    #url(r'^metadata/edit/(?P<pkey>\d+).*?$', 'metadata_edit_file', name='metadata_edit_file'),
                    #url(r'^metadata/show/(\d+)/(\d+){1,2}/(\d+)?/$', metadata_view),
                    )

#/searcher/editmetadata/324175101/1//
# ## Show all images for a certain Product
# (r'^products/show/(?P<product_id>\d+)/$', products_view),
# ## Add Delete and Show Tagging info
# (r'^tag/show/(?P<image_id>\d+)/$', tagging_view),
# (r'^tag/edit/(?P<image_id>\d+)/$', tagging_view),
# (r'^tag/delete/(?P<image_id>\d+)/$', tagging_view),

# ## Pil and imagick functions to alter and save copies or thumbs
# (r'^image/process/(?P<image_id>\d+)/$', image_process_view),

# ## selects for editorial and production shoots / selections/collectionsgrouos/albums
# (r'^image/select/editorial/(?P<image_id>\d+)/$', image_selecteditorial_view),
# (r'^image/select/production/(?P<image_id>\d+)/$', image_selectproduction_view),

# (r'^image/show/editorial/(?P<image_id>\d+)/$', image_selecteditorial_view),
# (r'^image/show/production/(?P<image_id>\d+)/$', image_selectproduction_view),

# (r'^image/remove/editorial/(?P<image_id>\d+)/$', image_selecteditorial_view),
# (r'^image/remove/production/(?P<image_id>\d+)/$', image_selectproduction_view),

from searcher.models import PostReadyOriginal
# from django.conf.urls import defaults
from django.views.generic.dates import ArchiveIndexView
import searcher.views
from searcher.views import PhotoYearArchiveView, PhotoMonthArchiveView, PhotoWeekArchiveView, PhotoDayArchiveView
# postreadyorig_info = {
#     "queryset"   : PostReadyOriginal.objects.all(),
#     "date_field" : "photo_date"
# }

## All
urlpatterns += patterns('searcher.views',
    url(r'^postreadyorig/$', ArchiveIndexView.as_view(
      model=PostReadyOriginal,
      date_field="photo_date",
      template_name="genericviews/photo_orig_archive.html"),
      name="photo_orig_archive"),
)

## Year
urlpatterns += patterns('searcher.views',
    url(r'^postreadyorig/(?P<year>\d{4})/$',
        PhotoYearArchiveView.as_view(
        template_name="genericviews/photo_orig_archive_year.html"),
        name="photo_orig_archive_year"),
)

## Week
urlpatterns += patterns('searcher.views',
    url(r'^postreadyorig/(?P<year>\d{4})/week/(?P<week>\d+)/$',
        PhotoWeekArchiveView.as_view(
        template_name="genericviews/photo_orig_archive_week.html"),
        name="photo_orig_archive_week"),
)

## Month
urlpatterns += patterns('searcher.views',
    url(r'^postreadyorig/(?P<year>\d{4})/(?P<month>[-\w]+)/$',
        PhotoMonthArchiveView.as_view(
        template_name="genericviews/photo_orig_archive_month.html"),
        name="photo_orig_archive_month"),
    # Example: /2012/08/
    url(r'^postreadyorig/(?P<year>\d{4})/(?P<month>\d+)/$',
        PhotoMonthArchiveView.as_view(
        month_format='%m',
        template_name="genericviews/photo_orig_archive_month.html"),
        name="photo_orig_archive_month_numeric"),
)

## Day
urlpatterns += patterns('searcher.views',
    url(r'^postreadyorig/(?P<year>\d{4})/(?P<month>\d+)/(?P<day>\d{2})/$',
        PhotoDayArchiveView.as_view(
        month_format='%m',
        template_name="genericviews/photo_orig_archive_day.html"),
        name="photo_orig_archive_day"),
)


from django.conf.urls import patterns, url
#from django.views.generic import direct_to_template
from django.shortcuts import render_to_response
from django.views.generic import TemplateView

urlpatterns += patterns('searcher.views',
    url(r'^imagenotes$', TemplateView.as_view(template_name='searcher/forms/imagenotes_form.html'), name="imagenotes_form"),
    #url(r'^imagenotes/$', 'imagenotes_form', name="imagenotes_form"),
    # url(r'^imagenotes/success/$', direct_to_template, {'template': 'base/success.html'},
    #     name="imagenotes_success"),
)


#
#   (r'^$', 'django.views.generic.list_detail.object_list', info_dict),
#   (r'^(?P<object_id>\d+)/$', 'django.views.generic.ListView.as_view()', info_dict),

###### All RAW Generic Views
from searcher.models import ProductionRawZimages
import django.conf.urls
from django.views.generic.dates import ArchiveIndexView
import searcher.views
from searcher.views import PhotoRawYearArchiveView, PhotoRawMonthArchiveView, PhotoRawWeekArchiveView, PhotoRawDayArchiveView
# prodrawonfig_info = {
#     "queryset"   : ProductionRawOnfigure.objects.all(),
#     "date_field" : "photo_date"
# }

## All
urlpatterns += patterns('searcher.views',
    url(r'^prodrawonfig/$', ArchiveIndexView.as_view(
      model=ProductionRawZimages,
      date_field="photo_date",
      template_name="genericviews/photo_orig_archive.html"),
      name="photo_raw_archive"),
)

## Year
urlpatterns += patterns('searcher.views',
    url(r'^prodrawonfig/(?P<year>\d{4})/$',
        PhotoRawYearArchiveView.as_view(
        template_name="genericviews/photo_orig_archive_year.html"),
        name="photo_raw_archive_year"),
)

## Week
urlpatterns += patterns('searcher.views',
    url(r'^prodrawonfig/(?P<year>\d{4})/week/(?P<week>\d+)/$',
        PhotoRawWeekArchiveView.as_view(
        template_name="genericviews/photo_orig_archive_week.html"),
        name="photo_raw_archive_week"),
)

## Month
urlpatterns += patterns('searcher.views',
    url(r'^prodrawonfig/(?P<year>\d{4})/(?P<month>[-\w]+)/$',
        PhotoRawMonthArchiveView.as_view(
        template_name="genericviews/photo_orig_archive_month.html"),
        name="photo_raw_archive_month"),
    # Example: /2012/08/
    url(r'^prodrawonfig/(?P<year>\d{4})/(?P<month>\d+)/$',
        PhotoMonthArchiveView.as_view(
        month_format='%m',
        template_name="genericviews/photo_orig_archive_month.html"),
        name="photo_raw_archive_month_numeric"),
)

## Day
urlpatterns += patterns('searcher.views',
    url(r'^prodrawonfig/(?P<year>\d{4})/(?P<month>\d+)/(?P<day>\d{2})/$',
        PhotoRawDayArchiveView.as_view(
        month_format='%m',
        template_name="genericviews/photo_orig_archive_day.html"),
        name="photo_orig_archive_day"),
)



# ## Tasty pie api
# # urls.py
# from searcher.api.resources import ProductSnapshotLiveResource
# #
# productsnapshotlive_resource = ProductSnapshotLiveResource()
# urlpatterns += patterns(
#      # The normal jazz here...
#        #(r'^selectedapi/', include('searcher.urls')),
#        (r'^api/', include(productsnapshotlive_resource.urls)),
# )

from django.conf.urls import patterns, url
from djdam.settings import MEDIA_ROOT

# urlpatterns += patterns('',
#                         url(r'^excel/list/$',
#                             'searcher.views.list',
#                             name='list'),
# )

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += patterns('',
                        url(r'^excel/upload/$',
                            'searcher.file-views.upload_home',
                            name='fileupload'),
                        ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


## Script Running from Modal Forms on HomePg
urlpatterns += patterns('',

    url(r'^runscripts/script_runner_home/?.*?$',
        'searcher.run-script-views.script_runner_home_page',
        name='script_runner'),

    url(r'^searcher/utils/meckPM_localLoginSave.py/?.*?(?P<styles_list>.+)$',
        'searcher.run-script-views.script_runner_home_page',
        name='meckPM_localLoginSave'),

    url(r'^searcher/utils/download_server_imgs_byPOorStyleList.py/?.*?(?P<ponum>\d+)$',
        'searcher.run-script-views.script_runner_home_page',
        name='download_server_imgs_byPOorStyleList'),

    url(r'^searcher/utils/newAll_Sites_CacheClear.py/?.*?(?P<styles_list>.+)$',
        'searcher.run-script-views.script_runner_home_page',
        name='newAll_Sites_CacheClear'),

    url(r'^searcher/utils/bfly_listpage_scrape_clear.py/?.*?(?P<bfly_url>.+)$',
        'searcher.run-script-views.script_runner_home_page',
        name='bfly_listpage_scrape_clear'),

    url(r'^searcher/utils/bflyurl_scrape_return_styles_only/?.*?(?P<bfly_url>.+)$',
        'searcher.run-script-views.script_runner_home_page',
        name='bflyurl_scrape_return_styles_only'),

)

