__author__ = 'johnb'
import autocomplete_light
from searcher.models import ProductSnapshotLive

# This will generate a ProductSnapshotLiveAutocomplete class
autocomplete_light.register(ProductSnapshotLive,
    # Just like in ModelAdmin.search_fields
    search_fields=['^colorstyle', 'brand', 'vendor_style'],
    # This will actually html attribute data-placeholder which will set
    # javascript attribute widget.autocomplete.placeholder.
    autocomplete_js_attributes={'placeholder': 'Other model name ?',},
)

class ScriptRunnerAutocomplete(autocomplete_light.AutocompleteListTemplate):
    choices = ['download_server_imgs_byPOorStyleList',
               'newAll_Sites_CacheClear',
               'bfly_listpage_scrape_clear',
               'bflyurl_scrape_return_styles_only',
               'meckPM_localLoginSave']
    autocomplete_template = 'autocompletelight/scriptchoose_hardcoded_autocomplete_box.html'
autocomplete_light.register(ScriptRunnerAutocomplete)


import autocomplete_light
from models import ProductSnapshotLive, SupplierIngestImages
class PoNumberAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['^colorstyle', 'po_number']
autocomplete_light.register(ProductSnapshotLive, PoNumberAutocomplete)

class ColorstyleAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['^colorstyle', 'po_number']
autocomplete_light.register(ProductSnapshotLive, ColorstyleAutocomplete)


class VendorNameAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['^colorstyle', 'vendor_name']
autocomplete_light.register(SupplierIngestImages, VendorNameAutocomplete)