# Register your models here.
from django.contrib import admin
import autocomplete_light
from models import ImageUpdate, SupplierIngestImages, SupplierIngest

class ImageUpdateAdmin(admin.ModelAdmin):
    # This will generate a ModelForm
    form = autocomplete_light.modelform_factory(ImageUpdate)
admin.site.register(ImageUpdate, ImageUpdateAdmin)


class SupplierIngestImagesAdmin(admin.ModelAdmin):
    # This will generate a ModelForm
    form = autocomplete_light.modelform_factory(SupplierIngestImages)
admin.site.register(SupplierIngestImages, SupplierIngestImagesAdmin)


class SupplierIngestAdmin(admin.ModelAdmin):
    # This will generate a ModelForm
    form = autocomplete_light.modelform_factory(SupplierIngest)
admin.site.register(SupplierIngest, SupplierIngestAdmin)