#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'johnb'

# ## django rest framework
# {% block script %}
# {{ block.super }}
# {% include 'autocomplete_light/static.html' %}
# {% endblock %}
#
#
# ##You can now add the autocomplete_light.ChoiceWidget widget to the serializer field.
#
# #import autocomplete_light
#
# class BookSerializer(serializers.ModelSerializer):
#     author = serializers.ChoiceField(
#         widget=autocomplete_light.ChoiceWidget('AuthorAutocomplete')
#     )
#
#     class Meta:
#         model = Book
#
#

## tastypie
## Create an api directory in your app with a bare __init__.py.

# Create an searcher/api/resources.py file and place the following in it:
# searcher/api/resources.py
from django.contrib.auth.models import User
from django.conf.urls import *
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.serializers import Serializer
from tastypie import fields
## Data Models
from searcher.models import SelectedFiles, ProductSnapshotLive, OffshoreStatus, ProductionRawCp1Data, ExcelToolData, ViewExcelToolDuplicateVendorStyle
## File Models
from searcher.models import Zimages1Photoselects, PostReadyOriginal, PushPhotoselects, ProductionRawZimages, SupplierIngest, SupplierIngestImages
from tastypie.throttle import BaseThrottle, CacheThrottle

## User and Session Resources
class UserResource(ModelResource):
    class Meta:
        serializer = Serializer(formats=['json', 'jsonp', 'xml'])
        queryset = User.objects.all()
        resource_name = 'user'
        allowed_methods = ['get']
        #fields = ['username', 'first_name', 'last_name', 'last_login']
        #instead of Excluding like below blklist above fields acts as whitelist
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        throttle = BaseThrottle(throttle_at=100)

class SelectedFilesResource(ModelResource):
    # user = fields.ForeignKey(UserResource, 'user')
    class Meta:
        serializer = Serializer(formats=['json', 'jsonp', 'xml'])
        resource_name = 'files-user-selected'
        # authorization= Authorization()
        queryset = SelectedFiles.objects.all()
        allowed_methods = ['get', 'post', 'put']
        detail_allowed_methods = ['get']

#
## File Path Resources
class ProductionRawZimagesResource(ModelResource):
    # user = fields.ForeignKey(UserResource, 'user')
    class Meta:
        serializer = Serializer(formats=['json', 'jsonp', 'xml'])
        resource_name = 'raw-fullsize'
        # authorization= Authorization()
        queryset = ProductionRawZimages.objects.all()
        allowed_methods        = ['get', 'post']
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get']


class PushPhotoselectsResource(ModelResource):
    # user = fields.ForeignKey(UserResource, 'user')
    class Meta:
        serializer = Serializer(formats=['json', 'jsonp', 'xml'])
        resource_name = 'selects-push'
        # authorization= Authorization()
        queryset = PushPhotoselects.objects.all()
        allowed_methods = ['get', 'post', 'put']
        detail_allowed_methods = ['get']

class Zimages1PhotoselectsResource(ModelResource):
    # user = fields.ForeignKey(UserResource, 'user')
    class Meta:
        serializer = Serializer(formats=['json', 'jsonp', 'xml'])
        resource_name = 'selects-thumb'
        # authorization= Authorization()
        queryset =  Zimages1Photoselects.objects.all()
        allowed_methods        = ['get', 'post']
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get']

class PostReadyOriginalResource(ModelResource):
    # user = fields.ForeignKey(UserResource, 'user')
    class Meta:
        serializer = Serializer(formats=['json', 'jsonp', 'xml'])
        resource_name = 'selects-fullsize'
        # authorization= Authorization()
        queryset =  PostReadyOriginal.objects.all()
        allowed_methods        = ['get', 'post']
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get']

#
### Data Resources

class ProductSnapshotLiveResource(ModelResource):
    class Meta:
        queryset = ProductSnapshotLive.objects.all()
        allowed_methods = ['get']
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        resource_name = 'pmdata'
        detail_uri_name = 'colorstyle'
        serializer = Serializer(formats=['json', 'jsonp', 'xml', 'yaml', 'html', 'plist'])

        # to have generated url go to searcher/api not root url/api
        #resource_name = 'searcher/pmdata'
        #authorization = DjangoAuthorization()
        # filtering = {
        #     'slug': ALL,
        #     'user': ALL_WITH_RELATIONS,
        #     'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        #     'gender': ALL,
        # }

    def dispatch(self, request_type, request, **kwargs):
        colorstyle = kwargs.pop('colorstyle')
        kwargs['colorstyle'] = get_object_or_404(ProductSnapshotLive, colorstyle=colorstyle)
        return super(ProductSnapshotLiveResource, self).dispatch(request_type, request, **kwargs)

    # def prepend_urls(self):
    #             return [
    #                 url(r"^(?P<pmdata>{0})/(?P<colorstyle>{1})/$".format(self._meta.exceltooldata), self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
    #             ]


### Supplier Ingestion Data incl Vendor Image Urls
class SupplierIngestResource(ModelResource):
    # user = fields.ForeignKey(UserResource, 'user')
    class Meta:
        serializer = Serializer(formats=['json', 'jsonp', 'xml'])
        resource_name = 'suppler-ingest'
        # authorization= Authorization()
        queryset = SupplierIngest.objects.all()  # .filter(cp1_colortag__icontains='YELLOW')
        allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get']
        excludes = ['active', 'create_dt', 'start_dt']
        filtering = {
            'colorstyle': ALL_WITH_RELATIONS,
            'alt': ALL_WITH_RELATIONS,
            'vendor_style': ALL,
            'modify_dt': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
            'po_number': ALL,
        }


    def dispatch(self, request_type, request, **kwargs):
        colorstyle = kwargs.pop('colorstyle')
        alt        = kwargs.pop('alt')
        kwargs['colorstyle'] = get_object_or_404(SupplierIngest, colorstyle=colorstyle)
        kwargs['alt'] = get_object_or_404(SupplierIngest, alt=alt)
        return super(SupplierIngestResource, self).dispatch(request_type, request, **kwargs)


### Supplier Ingestion Data incl Vendor Image Urls
class SupplierIngestImagesResource(ModelResource):
    # user = fields.ForeignKey(UserResource, 'user')
    class Meta:
        serializer = Serializer(formats=['json', 'jsonp', 'xml'])
        resource_name = 'suppler-ingest'
        # authorization= Authorization()
        queryset = SupplierIngest.objects.all()  # .filter(cp1_colortag__icontains='YELLOW')
        allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get']
        excludes = ['active', 'create_dt', 'start_dt']
        #fields = ['file_name', 'colorstyle', 'alt', 'image_url','bfly_local_src', 'bfly_zoom_src' ]
        filtering = {
            'colorstyle': ALL,
            'alt': ALL,
            'vendor_style': ALL,
            'modified_dt': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
            'vendor_name': ALL,
        }


    def dispatch(self, request_type, request, **kwargs):
        colorstyle = kwargs.pop('colorstyle')
        alt        = kwargs.pop('alt')
        kwargs['colorstyle'] = get_object_or_404(SupplierIngestImages, colorstyle=colorstyle)
        kwargs['alt'] = get_object_or_404(SupplierIngestImages, alt=alt)
        return super(SupplierIngestImagesResource, self).dispatch(request_type, request, **kwargs)


class OffshoreStatusResource(ModelResource):
    class Meta:
        resource_name = 'offshore-style'
        queryset = OffshoreStatus.objects.all()
        allowed_methods = ['get', 'post', 'put']
        detail_uri_name = 'colorstyle'

    def dispatch(self, request_type, request, **kwargs):
        colorstyle = kwargs.pop('colorstyle')
        kwargs['colorstyle'] = get_object_or_404(OffshoreStatus, colorstyle=colorstyle)
        return super(OffshoreStatusResource, self).dispatch(request_type, request, **kwargs)


class OffshoreStatusSentOnlyResource(ModelResource):
    class Meta:
        resource_name = 'offshore-sent'
        queryset = OffshoreStatus.objects.all().exclude(send_dt=None).filter(return_dt=None)
        allowed_methods = ['get', 'post']
        detail_uri_name = 'colorstyle'

    def dispatch(self, request_type, request, **kwargs):
        colorstyle = kwargs.pop('colorstyle')
        kwargs['colorstyle'] = get_object_or_404(OffshoreStatus, colorstyle=colorstyle)
        return super(OffshoreStatusSentOnlyResource, self).dispatch(request_type, request, **kwargs)


### Raw Capture 1 data
class ProductionRawCp1DataResource(ModelResource):
    # user = fields.ForeignKey(UserResource, 'user')
    class Meta:
        serializer = Serializer(formats=['json', 'jsonp', 'xml'])
        resource_name = 'raw-cp1-data'
        authorization= Authorization()
        queryset = ProductionRawCp1Data.objects.all()
        allowed_methods        = ['get', 'post']
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get']

class ProductionRawCp1PreSelectResource(ModelResource):
    # user = fields.ForeignKey(UserResource, 'user')
    class Meta:
        serializer = Serializer(formats=['json', 'jsonp', 'xml'])
        resource_name = 'raw-cp1-preselect'
        authorization= Authorization()
        queryset = ProductionRawCp1Data.objects.all().filter(cp1_colortag__icontains='YELLOW')
        allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get']

class ProductionRawCp1SelectResource(ModelResource):
    # user = fields.ForeignKey(UserResource, 'user')
    class Meta:
        serializer = Serializer(formats=['json', 'jsonp', 'xml'])
        resource_name = 'raw-cp1-select'
        authorization= Authorization()
        queryset = ProductionRawCp1Data.objects.all().filter(cp1_colortag__icontains='GREEN')
        allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get']


class ExcelToolDataResource(ModelResource):
    #exceltooldata = ''#fields.ForeignKey(ExcelToolDataResource, 'view_excel_tool_duplicate_vendor_style')

    class Meta:
        serializer = Serializer(formats=['json', 'jsonp', 'xml'])
        resource_name = 'excel-tool-data'
        detail_uri_name = 'colorstyle'
        #authorization = Authorization()
        queryset = ExcelToolData.objects.all() #.filter(vendor_style__icontains='')
        allowed_methods = ['get','post']
        detail_allowed_methods = ['get','post']
        list_allowed_methods = ['get','post']
        filtering = {
            'colorstyle': ALL,
            'vendor_style': ALL,
            'modify_dt': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
            'po_number': ALL,
        }

    # def prepend_urls(self):
    #         return [
    #             url(r"^(?P<'excel-tool-data'>%s)/(?P<colorstyle>[\w\d_.-]+)/$" % self._meta.exceltooldata,
    #                                                                              self.wrap_view('dispatch_detail'),
    #                                                                              name="api_dispatch_detail"),
    #         ]


    def dispatch(self, request_type, request, **kwargs):
        colorstyle = kwargs.pop('colorstyle')
        kwargs['colorstyle'] = get_object_or_404(ExcelToolData, colorstyle=colorstyle)
        return super(ExcelToolDataResource, self).dispatch(request_type, request, **kwargs)

    # def get_object_list(self, request):
    #     vendor_style = request.POST['vendor_style']
    #     colorstyle   = request.POST['colorstyle']
    #     input_list   = request.POST['input_list']
    #
    #     if input_list:
    #         return super(ExcelToolDataResource, self).get_object_list(request).filter(colorstyle__in=input_list)
    #     elif vendor_style:
    #         return super(ExcelToolDataResource, self).get_object_list(request).filter(vendor_style__icontains=vendor_style)
    #     elif colorstyle:
    #         return super(ExcelToolDataResource, self).get_object_list(request).filter(colorstyle__exact=colorstyle)
    #     else:
    #         return super(ExcelToolDataResource, self).get_object_list(request).filter(vendor_style__in=input_list)


from django.shortcuts import get_object_or_404

class ViewExcelToolDuplicateVendorStyleResource(ModelResource):
    exceltooldata = fields.ForeignKey(ExcelToolDataResource, 'excel-tool-data')

    class Meta:
        serializer = Serializer(formats=['json', 'jsonp', 'xml'])
        queryset = ViewExcelToolDuplicateVendorStyle.objects.all()
        detail_uri_name = 'colorstyle'
        resource_name = 'duplicate-vendor-style'
        allowed_methods = ['get','post']
        detail_allowed_methods = ['get','post']
        list_allowed_methods = ['get','post']
        filtering = {
            'colorstyle': ALL,
            'vendor_style': ('exact', 'startswith',),  #ALL,
            #'modify_dt': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
            'color_group_id': ALL_WITH_RELATIONS,
        }


    # def dispatch(self, request_type, request, **kwargs):
    #     colorstyle = kwargs.pop('colorstyle')
    #     kwargs['colorstyle'] = get_object_or_404(ExcelToolData, colorstyle=colorstyle)
    #     return super(ViewExcelToolDuplicateVendorStyleResource, self).dispatch(request_type, request, **kwargs)

    #
    # def get_object_list(self, request):
    #     vendor_style = request.POST['vendor_style']
    #     colorstyle = request.POST['colorstyle']
    #     return super(ViewExcelToolDuplicateVendorStyleResource, self).get_object_list(request).filter(
    #         vendor_style__exact=vendor_style)

    # def prepend_urls(self):
    #     return [url(r"^(?P<'excel-tool-data'>%s)/(?P<colorstyle>[\w\d_.-]+)/$" % self._meta.exceltooldata,
    #                                                                          self.wrap_view('dispatch_detail'),
    #                                                                          name="api_dispatch_detail"),
    #     ]

# class ViewExcelToolDuplicateVendorStyleResource(ModelResource):
#     class Meta:
#         serializer = Serializer(formats=['json', 'jsonp', 'xml'])
#         resource_name = 'view_excel_tool_duplicate_vendor_style'
#         #authorization = Authorization()
#         queryset = ViewExcelToolDuplicateVendorStyle.objects.all() #.filter(vendor_style__icontains='')
#         allowed_methods = ['get']
#         detail_allowed_methods = ['get']
#         list_allowed_methods = ['get']
#         filtering = {
#             'colorstyle': ALL_WITH_RELATIONS,
#             'vendor_style': ALL,
#             'modify_dt': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
#             'po_number': ALL,
#         }




#### Throttle exmpl
# class ProductSnapshotLiveResource(ModelResource):
#     class Meta:
#         resource_name = 'pmdata'
#         queryset = ProductSnapshotLive.objects.all()
#         allowed_methods = ['get']
#         throttle = CacheThrottle()

#     def prepend_urls(self):
#         return [
#             url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_search'), name="api_get_search"),
#         ]

#     def search(self, request, **kwargs):
#         self.method_check(request, allowed=self.Meta.allowed_methods)
#         self.is_authenticated(request)
#         self.throttle_check(request)
#         self.log_throttled_access(request)

#         # Do the query.
#         sqs = SearchQuerySet().models(ProductSnapshotLive).load_all().auto_query(request.GET.get('q', ''))
#         paginator = Paginator(sqs, 20)

#         try:
#             page = paginator.page(int(request.GET.get('page', 1)))
#         except InvalidPage:
#             raise Http404("Sorry, no results on that page.")

#         objects = []

#         for result in page.object_list:
#             bundle = self.build_bundle(obj=result.object, request=request)
#             bundle = self.full_dehydrate(bundle)
#             objects.append(bundle)

#         object_list = {
#             'objects': objects,
#         }

#         return self.create_response(request, object_list)
