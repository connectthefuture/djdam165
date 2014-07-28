__author__ = 'johnb'

import django_tables2 as tables
from searcher.models import SupplierIngest

# Def Tables -- aka tables.py
class SupplierIngestTable(tables.Table):
    class Meta:
        model = SupplierIngest
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}


##### VIEWS ####
from django.shortcuts import render
from django_tables2   import RequestConfig


def suppliers(request):
    table = SupplierIngestTable(SupplierIngest.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'supplier-ingest-styles.html', {'table': table})
