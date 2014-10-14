# Register your models here.
import searcher.admin_custom as myadmin
myadmin.autodiscover()
import autocomplete_light
from models import *

from django.contrib.admin.filters import SimpleListFilter
#
# class NullFilterSpec(SimpleListFilter):
#     title = u''
#
#     parameter_name = u''
#
#     def lookups(self, request, model_admin):
#         return (
#             ('1', _('Has value'), ),
#             ('0', _('None'), ),
#         )
#
#     def queryset(self, request, queryset):
#         kwargs = {
#         '%s'%self.parameter_name : None,
#         }
#         if self.value() == '0':
#             return queryset.filter(**kwargs)
#         if self.value() == '1':
#             return queryset.exclude(**kwargs)
#         return queryset
#

#from django.contrib.admin.filters import BooleanFieldListFilter
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

# FilterSpec.register places the new FilterSpec at the back
# of the list. This can be a problem, because the first
# matching FilterSpec is the one used.
def _register_front(cls, test, factory):
    cls.filter_specs.insert(0, (test, factory))
FilterSpec =BooleanFieldListFilter
FilterSpec.register_front = classmethod(_register_front)

class NullFilterSpec(FilterSpec):
    fields = (models.CharField, models.DateField, models.DateTimeField)

    #@classmethod
    def test(cls, field):
        return field.null and isinstance(field, cls.fields) and not field._choices
    test = classmethod(test)

    def __init__(self, f, request, params, model, model_admin):
        super(NullFilterSpec, self).__init__(f, request, params, model, model_admin)
        self.lookup_kwarg = '%s__isnull' % f.name
        self.lookup_val = request.GET.get(self.lookup_kwarg, None)

    def choices(self, cl):
        # bool(v) must be False for IS NOT NULL and True for IS NULL, but can only be a string
        for k, v in ((_('All'), None), (_('Has value'), ''), (_('Omitted'), '1')):
            yield {
                'selected' : self.lookup_val == v,
                'query_string' : cl.get_query_string({self.lookup_kwarg : v}),
                'display' : k
            }

FilterSpec.register_front(NullFilterSpec.test, NullFilterSpec)
#
# class StartNullFilterSpec(NullFilterSpec):
#     title = u'Started'
#     parameter_name = u'started'


class ProductSnapshotLiveAdmin(myadmin.ModelAdmin):
    # This will generate a ModelForm
    list_display = ('admin_image', 'colorstyle', 'brand', 'product_type', 'po_number', 'vendor_style', 'image_ready_dt')
    search_fields = ['colorstyle__vendor_style__brand']
    list_filter = ('image_ready_dt', 'product_type',)
    form = autocomplete_light.modelform_factory(ProductSnapshotLive)
myadmin.site.register(ProductSnapshotLive, ProductSnapshotLiveAdmin)


class SupplierIngestImagesAdmin(myadmin.ModelAdmin):
    # This will generate a ModelForm
    list_display = ('bfly_image', 'colorstyle', 'alt', 'modified_dt', 'vendor_image')
    search_fields = ['colorstyle__vendor_name']
    list_filter = (('modified_dt', FilterSpec), 'vendor_name')
    form = autocomplete_light.modelform_factory(SupplierIngestImages)
myadmin.site.register(SupplierIngestImages, SupplierIngestImagesAdmin)


from django.contrib.admin import BooleanFieldListFilter
class SupplierIngestAdmin(myadmin.ModelAdmin):
    # This will generate a ModelForm
    list_display = ('bfly_image', 'vendor_image', 'colorstyle', 'vendor_name', 'vendor_style', 'image_url', 'image_ready_dt', 'modified_dt', 'version', 'get_http_status_code')
    search_fields = ['colorstyle','vendor_name']
    list_filter = (('image_ready_dt', BooleanFieldListFilter), 'modified_dt', 'vendor_name')
    #form = autocomplete_light.modelform_factory(SupplierIngest)
    # def get_search_results(self, request, queryset, search_term):
    #     queryset, use_distinct = super(SupplierIngestAdmin, self).get_search_results(request, queryset, search_term)
    #     try:
    #         search_term_as_int = int(search_term)
    #     except ValueError:
    #         pass
    #     else:
    #         queryset |= self.model.objects.filter(age=search_term_as_int)
    #     return queryset, use_distinct
myadmin.site.register(SupplierIngest, SupplierIngestAdmin)


class ImageUpdateAdmin(myadmin.ModelAdmin):
    # This will generate a ModelForm
    list_display = ('colorstyle', 'alt', 'modify_dt')
    search_fields = ['colorstyle__alt']
    form = autocomplete_light.modelform_factory(ImageUpdate)
myadmin.site.register(ImageUpdate, ImageUpdateAdmin)


class OffshoreStatusAdmin(myadmin.ModelAdmin):
    # This will generate a ModelForm
    list_display = ('colorstyle', 'category', 'product_type', 'return_dt')
    search_fields = ['colorstyle', 'send_dt', 'return_dt']
    form = autocomplete_light.modelform_factory(OffshoreStatus)
myadmin.site.register(OffshoreStatus, OffshoreStatusAdmin)


########## Primary Admins End
### Image Admins


class PostReadyOriginalAdmin(myadmin.ModelAdmin):
    # This will generate a ModelForm
    list_display = ('primary_select_image', 'colorstyle', 'alt', 'photo_date', 'file_path')
    search_fields = ['colorstyle']
    form = autocomplete_light.modelform_factory(PostReadyOriginal)
myadmin.site.register(PostReadyOriginal, PostReadyOriginalAdmin)


class PushPhotoselectsAdmin(myadmin.ModelAdmin):
    # This will generate a ModelForm
    list_display = ('primary_select_image', 'colorstyle', 'alt', 'photo_date', 'file_path')
    search_fields = ['colorstyle']
    form = autocomplete_light.modelform_factory(PushPhotoselects)
myadmin.site.register(PushPhotoselects, PushPhotoselectsAdmin)


class Zimages1PhotoselectsAdmin(myadmin.ModelAdmin):
    # This will generate a ModelForm
    list_display = ('primary_select_image', 'colorstyle', 'alt', 'photo_date', 'file_path')
    search_fields = ['colorstyle']
    form = autocomplete_light.modelform_factory(Zimages1Photoselects)
myadmin.site.register(Zimages1Photoselects, Zimages1PhotoselectsAdmin)


class ProductionRawOnfigureAdmin(myadmin.ModelAdmin):
    # This will generate a ModelForm
    list_display = ('primary_select_image', 'colorstyle', 'alt', 'shot_number', 'photo_date', 'file_path')
    search_fields = ['colorstyle']
    form = autocomplete_light.modelform_factory(ProductionRawOnfigure)
myadmin.site.register(ProductionRawOnfigure, ProductionRawOnfigureAdmin)


########## Image Admins End
### Data Admins

class ExcelToolDataAdmin(myadmin.ModelAdmin):
    # This will generate a ModelForm
    form = autocomplete_light.modelform_factory(ExcelToolData)
myadmin.site.register(ExcelToolData, ExcelToolDataAdmin)


class ProductAdmin(myadmin.ModelAdmin):
    # This will generate a ModelForm
    form = autocomplete_light.modelform_factory(Product)
myadmin.site.register(Product, ProductAdmin)


class VendorAdmin(myadmin.ModelAdmin):
    list_display = ('vendor_name', 'website', 'ftpurl_prefix')
    search_fields = ['vendor_name']
    form = autocomplete_light.modelform_factory(Vendor)
myadmin.site.register(Vendor, VendorAdmin)


######## End Data Admins
### Depreciated/Etc
class SelectedFilesAdmin(myadmin.ModelAdmin):
    # This will generate a ModelForm
    form = autocomplete_light.modelform_factory(SelectedFiles)
myadmin.site.register(SelectedFiles, SelectedFilesAdmin)


##########
### Auth Groups and Users for Super only
class AuthGroupAdmin(myadmin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name',)
    form = autocomplete_light.modelform_factory(AuthGroup)
myadmin.site.register(AuthGroup, AuthGroupAdmin)


class AuthUserAdmin(myadmin.ModelAdmin):
    search_fields = ['username']
    list_display = ('username', 'is_staff', 'is_superuser', 'email')
    form = autocomplete_light.modelform_factory(AuthUser)
myadmin.site.register(AuthUser, AuthUserAdmin)


class AuthGroupPermissionsAdmin(myadmin.ModelAdmin):
    search_fields = ['group']
    list_display = ('id', 'group', 'permission')
    form = autocomplete_light.modelform_factory(AuthGroupPermissions)
myadmin.site.register(AuthGroupPermissions, AuthGroupPermissionsAdmin)