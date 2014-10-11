# Register your models here.
import searcher.admin_custom as myadmin
myadmin.autodiscover()
import autocomplete_light
from models import *


class ImageUpdateAdmin(myadmin.ModelAdmin):
    # This will generate a ModelForm
    list_display = ('colorstyle', 'alt', 'modify_dt')
    search_fields = ['colorstyle__alt']
    form = autocomplete_light.modelform_factory(ImageUpdate)
myadmin.site.register(ImageUpdate, ImageUpdateAdmin)


class SupplierIngestImagesAdmin(myadmin.ModelAdmin):
    # This will generate a ModelForm
    list_display = ('colorstyle', 'alt', 'modify_dt')
    search_fields = ['colorstyle__vendor_name']
    form = autocomplete_light.modelform_factory(SupplierIngestImages)
myadmin.site.register(SupplierIngestImages, SupplierIngestImagesAdmin)


class SupplierIngestAdmin(myadmin.ModelAdmin):
    # This will generate a ModelForm
    list_display = ('colorstyle', 'vendor_name', 'vendor_style','image_url', 'image_ready_dt', 'modified_dt', 'version')
    search_fields = ['colorstyle__vendor_name__vendor_brand']
    list_filter = ('vendor_name', 'vendor_brand', 'modified_dt')
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


class ProductSnapshotLiveAdmin(myadmin.ModelAdmin):
    # This will generate a ModelForm
    list_display = ('colorstyle', 'brand', 'product_type', 'po_number', 'vendor_style', 'image_ready_dt')
    search_fields = ['colorstyle__vendor_style__brand']
    form = autocomplete_light.modelform_factory(ProductSnapshotLive)
myadmin.site.register(ProductSnapshotLive, ProductSnapshotLiveAdmin)


class ExcelToolDataAdmin(myadmin.ModelAdmin):
    # This will generate a ModelForm
    form = autocomplete_light.modelform_factory(ExcelToolData)
myadmin.site.register(ExcelToolData, ExcelToolDataAdmin)


class ProductAdmin(myadmin.ModelAdmin):
    # This will generate a ModelForm
    form = autocomplete_light.modelform_factory(Product)
myadmin.site.register(Product, ProductAdmin)


class SelectedFilesAdmin(myadmin.ModelAdmin):
    # This will generate a ModelForm
    form = autocomplete_light.modelform_factory(SelectedFiles)
myadmin.site.register(SelectedFiles, SelectedFilesAdmin)


class OffshoreStatusAdmin(myadmin.ModelAdmin):
    # This will generate a ModelForm
    list_display = ('colorstyle', 'category', 'product_type', 'return_dt')
    search_fields = ['colorstyle', 'send_dt', 'return_dt']
    form = autocomplete_light.modelform_factory(OffshoreStatus)
myadmin.site.register(OffshoreStatus, OffshoreStatusAdmin)


class PostReadyOriginalAdmin(myadmin.ModelAdmin):
    # This will generate a ModelForm
    list_display = ('colorstyle', 'alt', 'photo_date', 'file_path')
    search_fields = ['colorstyle']
    form = autocomplete_light.modelform_factory(PostReadyOriginal)
myadmin.site.register(PostReadyOriginal, PostReadyOriginalAdmin)


### Auth Groups and Users for Super only
class AuthGroupAdmin(myadmin.ModelAdmin):
    form = autocomplete_light.modelform_factory(AuthGroup)
    pass
myadmin.site.register(AuthGroup, AuthGroupAdmin)


class AuthUserAdmin(myadmin.ModelAdmin):
    search_fields = ['username']
    list_display = ('username', 'is_staff', 'is_superuser', 'email')
    form = autocomplete_light.modelform_factory(AuthUser)
myadmin.site.register(AuthUser, AuthUserAdmin)
