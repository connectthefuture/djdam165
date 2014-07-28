__author__ = 'johnb'

import django_tables2 as tables
from searcher.models import SupplierIngest

####  Tables -- aka tables.py
class SupplierIngestTable(tables.Table):
    vendor_name  =  tables.Column()
    vendor_brand =  tables.Column()
    image_url	 =	tables.URLColumn()
    alt			 =	tables.Column()
    image_type 	 = 	tables.Column()


    class Meta:
        model = SupplierIngest
        # add class="paleblue" to <table> tag
        # attrs = {"class": "paleblue"}
        attrs = {"class": "table table-responsive"}



##### Table VIEWS ####
from django.shortcuts import render
from django_tables2   import RequestConfig


def get_http_status_code(request):
    import requests

    r = requests.get(request)
    code = r.status_code
    return code

def suppliers(request):
    table = SupplierIngest.objects.all()
    RequestConfig(request).configure(table)
    return render(request, 'tables/supplier-ingest-styles.html', {'table': table})
