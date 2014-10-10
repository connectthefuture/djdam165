# Register your models here.
from django.contrib import admin
import autocomplete_light
from models import *

class ImageUpdateAdmin(admin.ModelAdmin):
    # This will generate a ModelForm
    form = autocomplete_light.modelform_factory(ImageUpdate)
admin.site.register(ImageUpdate, ImageUpdateAdmin)


class SupplierIngestImagesAdmin(admin.ModelAdmin):
    # This will generate a ModelForm
    form = autocomplete_light.modelform_factory(SupplierIngestImages)
admin.site.register(SupplierIngestImages, SupplierIngestImagesAdmin)


class ProductSnapshotLiveAdmin(admin.ModelAdmin):
    # This will generate a ModelForm
    form = autocomplete_light.modelform_factory(ProductSnapshotLive)
admin.site.register(ProductSnapshotLive, ProductSnapshotLiveAdmin)


class ExcelToolDataAdmin(admin.ModelAdmin):
    # This will generate a ModelForm
    form = autocomplete_light.modelform_factory(ExcelToolData)
admin.site.register(ExcelToolData, ExcelToolDataAdmin)


class ProductAdmin(admin.ModelAdmin):
    # This will generate a ModelForm
    form = autocomplete_light.modelform_factory(Product)
admin.site.register(Product, ProductAdmin)


class SelectedFilesAdmin(admin.ModelAdmin):
    # This will generate a ModelForm
    form = autocomplete_light.modelform_factory(SelectedFiles)
admin.site.register(SelectedFiles, SelectedFilesAdmin)


class PostReadyOriginalAdmin(admin.ModelAdmin):
    # This will generate a ModelForm
    form = autocomplete_light.modelform_factory(PostReadyOriginal)
admin.site.register(PostReadyOriginal, PostReadyOriginalAdmin)