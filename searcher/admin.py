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
    list_display = ('colorstyle', 'image_number', 'vendor_name', 'vendor_brand')
    search_fields = ['colorstyle__vendor_name__vendor_brand']
    form = autocomplete_light.modelform_factory(SupplierIngest)
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