__author__ = 'johnb'

import django_tables2 as tables
from django_tables2 import RequestConfig, SingleTableView
from models import SupplierIngest, ProductSnapshotLive, PushPhotoselects
import itertools

####  Product Snapshot Tables
class ProductSnapshotLiveTable(tables.Table):
    from models import ProductSnapshotLive
    colorstyle       =  tables.Column(sortable=True)
    brand            =  tables.Column(orderable=True)
    vendor_style     =  tables.Column(sortable=True)
    color            =  tables.Column(orderable=True)
    image_url	     =	tables.URLColumn()  #'supplier_detail',args=[A('image_url')])
    sample_status 	 = 	tables.Column(orderable=True)
    sample_location  = 	tables.Column(sortable=True)
    track_number     =  tables.Column(sortable=True)
    po_type          =  tables.Column(orderable=True)

    def __init__(self, *args, **kwargs):
        super(ProductSnapshotLiveTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count()

    def render_urlcode(self):
        import requests
        r = requests.get(self.image_url)
        code = r.status_code
        return '<%d>' % code

    class Meta:
        model = ProductSnapshotLive
        # add class="paleblue" to <table> tag
        # attrs = {"class": "paleblue"}
        attrs = {"class": "table-responsive"}

####  Tables -- aka tables.py
class SupplierIngestTable(tables.Table):
    from models import SupplierIngest
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
        attrs = {"class": "table-responsive"}

##
# from django.views.generic import TemplateView
# class SupplierIngestTableView(TemplateView):
#     template_name = 'tables/supplier-ingest-detail.html'
#
#     def get_queryset(self, **kwargs):
#         return SupplierIngest.objects.all()
#
#     def get_context_data(self, **kwargs):
#         context = super(SupplierIngestTableView, self).get_context_data(**kwargs)
#         RequestConfig(self.request).configure(table)
#         context['filter'] = filter
#         context['table'] = table
#         return context


##### Table VIEWS ####
from django.shortcuts import render
from django_tables2 import RequestConfig, SingleTableView

def get_http_status_code(request):
    import requests

    r = requests.get(request)
    code = r.status_code
    return code


def suppliers(request):
    table = SupplierIngestTable(SupplierIngest.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'tables/supplier-ingest-styles.html', {'table': table})


def suppliers_compare(request):
    table = SupplierIngestTable(SupplierIngest.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'tables/supplier-ingest-styles.html', {'table': table})


def supplier_detail(request,vendor_brand=None,vendor_name=None):
    if not vendor_name and not vendor_brand:
        vendor_name = request.get['vendor_name']
        table = SupplierIngestTable(SupplierIngest.objects.all().filter(vendor_name__icontains=vendor_name))
    elif vendor_brand and not vendor_name:
        table = SupplierIngestTable(SupplierIngest.objects.all().filter(vendor_brand__icontains=vendor_brand))

    elif vendor_name:
        table = SupplierIngestTable(SupplierIngest.objects.all().filter(vendor_name__icontains=vendor_name))

    RequestConfig(request).configure(table)
    return render(request, 'tables/supplier-ingest-styles.html', {'table': table})


######## Filtered ####
import django_filters
class SupplierIngestFilter(django_filters.FilterSet):
    # vendor_name  = django_filters.AllValuesFilter()
    vendor_brand = django_filters.MultipleChoiceFilter()
    alt          = django_filters.RangeFilter()

    class Meta:
        model = SupplierIngest
        fields = ['vendor_name','vendor_brand','alt']
        order_by = ['vendor_name','vendor_brand','alt','colorstyle']

    def __init__(self, *args, **kwargs):
        super(SupplierIngestFilter, self).__init__(*args, **kwargs)
        self.filters['vendor_name'].extra.update(
            {'empty_label': 'All Vendors'})
        self.filters['vendor_brand'].extra.update(
            {'empty_label': 'All Brands'})
        self.filters['alt'].extra.update(
            {'empty_label': 'All Image Kinds'})

# class MySupplierFilter(django_filters.FilterSet):
#   field1 = django_filters.CharFilter()
#   field2 = django_filters.CharFilter()
#   field2 = django_filters.CharFilter()
#   field2 = django_filters.CharFilter()
#   field2 = django_filters.CharFilter()


######## Filtered Views #######
from django_tables2 import SingleTableView
from searcher.models import SupplierIngest


class FilteredSingleTableView(SingleTableView):
  def get_table_data(self):
    f = SupplierIngestFilter(self.request.GET, queryset = SupplierIngest.objects.all(), request=self.request )
    return f


  def get_context_data(self, **kwargs):
    context = super(FilteredSingleTableView, self).get_context_data(**kwargs)
    f = SupplierIngestFilter(self.request.GET, queryset = SupplierIngest.objects.all(), request=self.request )
    context['form'] = f.form
    return context


from django.shortcuts import render_to_response
def supplier_filter(request):
    f = SupplierIngestFilter(request.GET, queryset=SupplierIngest.objects.all())
    return render_to_response('searcher/tables/supplier-ingest-detail.html', {'filter': f})


# class FilteredSingleTableView(SingleTableView):
#   def get_table_data(self):
#     data= SupplierIngest.objects.all
#     if self.request.GET.get('field1'):
#       data = data.filter(field1=self.request.GET.get('field1') )
#     if self.request.GET.get('field1'):
#       data = data.filter(field1=self.request.GET.get('field1') )
#     return data
#
#     def get_context_data(self, **kwargs):
#       context = super(FilteredSingleTableView, self).get_context_data(**kwargs)
#       context['form'] = forms.MyFilterForm(self.request.user, self.request.GET)
#       return context


class SupplierIngestList(SingleTableView):
    model = SupplierIngest
    table_class = SupplierIngestTable