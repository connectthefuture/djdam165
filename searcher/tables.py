__author__ = 'johnb'

import django_tables2 as tables
from django_tables2 import RequestConfig, SingleTableView, A
from searcher.models import SupplierIngest
import itertools

####  Tables -- aka tables.py
class SupplierIngestTable(tables.Table):
    vendor_name  =  tables.Column()
    vendor_brand =  tables.Column()
    image_url	 =	tables.URLColumn()  #'supplier_detail',args=[A('image_url')])
    alt			 =	tables.Column()
    image_type 	 = 	tables.Column()

    def __init__(self, *args, **kwargs):
        super(SupplierIngestTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count()

    def render_urlcode(self):
        import requests
        r = requests.get(self.image_url)
        code = r.status_code
        return '<%d>' % code

    class Meta:
        model = SupplierIngest
        # add class="paleblue" to <table> tag
        # attrs = {"class": "paleblue"}
        attrs = {"class": "table table-responsive"}



##### Table VIEWS ####
from django.shortcuts import render
from django_tables2   import RequestConfig, SingleTableView, A


def get_http_status_code(request):
    import requests

    r = requests.get(request)
    code = r.status_code
    return code

def suppliers(request):
    table = SupplierIngestTable(SupplierIngest.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'tables/supplier-ingest-styles.html', {'table': table})


class SupplierIngestList(SingleTableView):
    model = SupplierIngest
    table_class = SupplierIngestTable