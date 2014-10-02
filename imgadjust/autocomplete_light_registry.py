__author__ = 'johnb'
import autocomplete_light
from searcher.models import SupplierIngestImages

# This will generate a SupplierIngestImagesAutocomplete class
autocomplete_light.register(SupplierIngestImages,
    # Just like in ModelAdmin.search_fields
    search_fields=['^colorstyle', 'vendor_name', 'vendor_style'],
    # This will actually html attribute data-placeholder which will set
    # javascript attribute widget.autocomplete.placeholder.
    autocomplete_js_attributes={'placeholder': 'Other model name ?',},
)
