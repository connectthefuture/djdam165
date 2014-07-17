#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Views for the base application """

from django.shortcuts import render


def home(request):
    """ Default view for the root """
    return render(request, 'base/jbhome.html',)



###### Testing Layout views
def bootstrapshell(request):
    """ Default view for the root """
    return render(request, 'base/bootstrapshell.html',)

def bootstrap3shell(request):
    """ Default view for the root """
    return render(request, 'base/bootstrap3shell.html',)

def testhome(request):
    """ Default view for the root """
    return render(request, 'base/jbtesthome.html',)


# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from searcher.forms import testJSONForm
pmdata_url = 'http://prodimages.ny.bluefly.com/api/v1/pmdata'

def testjsonform(request):
    import requests,os
    colorstyle = '321424701' #request.GET['data__0']
    #try:
    pmdata = requests.get(os.path.join(pmdata_url, colorstyle) + '/')
    #except:
    #    return
    json = [pmdata['colorstyle'],
            pmdata['po_number'],
            pmdata['vendor_style'],
            pmdata['product_type'],
            pmdata['product_subtype'],
            pmdata['color'],
            pmdata['brand']]
    form = testJSONForm(request.GET or None, initial={'data': json})
    if form.is_valid():
        # validate and save
        pass

    template = 'base/test_json_form.html'
    context = RequestContext(request, {'form': form})
    return render_to_response(template, context)



# "brand": "Gucci",
# "category": "",
# "color": "Brown",
# "colorstyle": "321424701",
# "copy_ready_dt": "2012-10-15",
# "gender": "",
# "image_ready_dt": "2012-10-16",
# "orig_start_dt": "2012-10-19",
# "po_number": "115696",
# "po_type": "Asset",
# "product_subtype": "Boots",
# "product_type": "Shoes",
# "production_complete_dt": "2012-10-16",
# "production_status": "Production Complete",
# "resource_uri": "/api/v1/pmdata/321424701/",
# "sample_id": "235056",
# "sample_image_dt": "2012-10-22",
# "sample_location": "warehouse",
# "sample_status": "Scanned Out to Warehouse",
# "sku": "891951821055",
# "sql_id": "101488919",
# "start_dt": "2012-10-26",
# "status_dt": "2012-10-17",
# "track_dt": "2012-10-17",
# "track_number": "1Z8FV4910392777189",
# "track_user": "tanya.aviles",
# "vendor_style": "295321 AC880 2160"