# Register your models here.
import searcher.admin_custom as myadmin
myadmin.autodiscover()
import autocomplete_light
from models import *


class ProductSnapshotLiveAdmin(myadmin.ModelAdmin):
    # This will generate a ModelForm
    list_display = ('admin_image', 'colorstyle', 'brand', 'product_type', 'po_number', 'vendor_style', 'image_ready_dt')
    search_fields = ['colorstyle__vendor_style__brand']
    form = autocomplete_light.modelform_factory(ProductSnapshotLive)
    list_filter = ('product_type', 'image_ready_dt',)
myadmin.site.register(ProductSnapshotLive, ProductSnapshotLiveAdmin)


class SupplierIngestImagesAdmin(myadmin.ModelAdmin):
    # This will generate a ModelForm
    list_display = ('bfly_image', 'colorstyle', 'alt', 'modified_dt', 'vendor_image')
    search_fields = ['colorstyle__vendor_name']
    list_filter = ('modified_dt', 'vendor_name')
    form = autocomplete_light.modelform_factory(SupplierIngestImages)
myadmin.site.register(SupplierIngestImages, SupplierIngestImagesAdmin)


class SupplierIngestAdmin(myadmin.ModelAdmin):
    # This will generate a ModelForm
    list_display = ('bfly_image', 'vendor_image', 'colorstyle', 'vendor_name', 'vendor_style', 'image_url', 'image_ready_dt', 'modified_dt', 'version', 'get_http_status_code')
    search_fields = ['colorstyle','vendor_name']
    list_filter = ('image_ready_dt', 'modified_dt', 'vendor_name')

form = autocomplete_light.modelform_factory(SupplierIngest)
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
    list_display = ('name','name__permission__name')
    form = autocomplete_light.modelform_factory(AuthGroup)
myadmin.site.register(AuthGroup, AuthGroupAdmin)


class AuthUserAdmin(myadmin.ModelAdmin):
    search_fields = ['username']
    list_display = ('username', 'is_staff', 'is_superuser', 'email')
    form = autocomplete_light.modelform_factory(AuthUser)
myadmin.site.register(AuthUser, AuthUserAdmin)
