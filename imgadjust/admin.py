__author__ = 'johnb'
import searcher.admin_custom as myadmin
myadmin.autodiscover()
import autocomplete_light
from models import *

from django.contrib.admin.filters import SimpleListFilter

class ProductAdmin(myadmin.ModelAdmin):
    # This will generate a ModelForm
    list_display = ('product_info__colorstyle', 'slug', 'vendor_name', 'vendor_brand', 'vendor_style', 'get_absolute_url')
    search_fields = ['vendor_style']
    list_filter = ('vendor_name')
    form = autocomplete_light.modelform_factory(Product)
myadmin.site.register(Product, ProductAdmin)


class ImageTypeAdmin(myadmin.ModelAdmin):
    # This will generate a ModelForm
    list_display = ('slug', 'colorstyle', 'alt')
    search_fields = ['colorstyle']
    list_filter = ('alt')
    form = autocomplete_light.modelform_factory(ImageType)
myadmin.site.register(ImageType, ImageTypeAdmin)


class ImageSourceAdmin(myadmin.ModelAdmin):
    # This will generate a ModelForm
    list_display = ('primary_select_image','colorstyle', 'source_url', 'supplier_ingest','vendor_image', 'bfly_image')
    search_fields = ['colorstyle']
    #list_filter = ('alt')
    form = autocomplete_light.modelform_factory(ImageSource)
myadmin.site.register(ImageSource, ImageSourceAdmin)