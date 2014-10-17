__author__ = 'johnb'
import autocomplete_light
from searcher.models import ProductSnapshotLive

# This will generate a ProductSnapshotLiveAutocomplete class
autocomplete_light.register(ProductSnapshotLive,
    # Just like in ModelAdmin.search_fields
    search_fields=['^colorstyle', 'brand', 'vendor_style'],
    # This will actually html attribute data-placeholder which will set
    # javascript attribute widget.autocomplete.placeholder.
    autocomplete_js_attributes={'placeholder': 'Whats my name ?',},
)

# class ScriptRunnerAutocomplete(autocomplete_light.AutocompleteListTemplate):
#     choices = ['download_server_imgs_byPOorStyleList',
#                'newAll_Sites_CacheClear',
#                'bfly_listpage_scrape_clear',
#                'bflyurl_scrape_return_styles_only',
#                'meckPM_localLoginSave']
#     autocomplete_template = 'autocompletelight/scriptchoose_hardcoded_autocomplete_box.html'
# autocomplete_light.register(ScriptRunnerAutocomplete)


import autocomplete_light
from models import ProductSnapshotLive, SupplierIngest


class ColorstyleAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['^colorstyle']

autocomplete_light.register(ProductSnapshotLive, ColorstyleAutocomplete,
        autocomplete_js_attributes = {
                                         'minimum_characters': 0,
        'placeholder': 'Colorstyle ?',
        },
        widget_js_attributes = {
        'max_values': 9,
        }
        )

class PoNumberAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['^colorstyle']

autocomplete_light.register(ProductSnapshotLive, PoNumberAutocomplete, autocomplete_js_attributes={
        'minimum_characters': 0,
        'placeholder': 'Po number ?',
    },
    widget_js_attributes = {
        'max_values': 6,
    }
    )


class VendorNameAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['^colorstyle', 'vendor_name']

autocomplete_light.register(SupplierIngest, VendorNameAutocomplete,
    autocomplete_js_attributes={
        'minimum_characters': 0,
        'placeholder': 'Vendor name ?',
    },
        widget_js_attributes={
        'max_values': 61,
    }
    )

import autocomplete_light

from models import TemplatedChoice

autocomplete_light.register(TemplatedChoice,
	autocomplete_light.AutocompleteModelTemplate,
	choice_template='template_autocomplete/templated_choice.html')