#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Views for the base application """

from django.shortcuts import render


def home(request):
    """ Default view for the root """
    return render(request, 'base/jbhome.html',)


#################
## REST framework
#################
from django.views.generic.base import TemplateView
class OnePageAppView(TemplateView):
    template_name = 'one_page_app.html'

def onepageappview(request):
    """ Default view for the root """
    return render(request, 'base/jbhome.html',)
#################
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

def ajaxexample(request):
    """ Default view for the root """
    return render(request, 'base/ajaxexample.html',)

def ajaxexample2(request):
    """ Default view for the root """
    from searcher.models import *
    try:
        colorstyle = request.GET['q']
        data = SupplierIngestImages.objects.filter(colorstyle__icontains=colorstyle)

        return render(request, 'base/ajaxexample.html', {'data': data})
    except:
        data = SupplierIngestImages.objects.all().order_by('-modified_dt', 'vendor_name', 'colorstyle', 'alt')[:100]
        return render(request, 'base/ajaxexample.html', {'data': data})

def ajaxdatatables(request):
    """ Default view for the root """
    from searcher.models import *
    try:
        colorstyle = request.GET['q']
        query = ProductSnapshotLive.objects.filter(colorstyle__icontains=colorstyle)
        return render(request, 'base/ajaxdatatables.html', {'data': data})
    except:
        data = ProductSnapshotLive.objects.all().order_by('-status_dt', '-colorstyle')[:100]
        return render(request, 'base/ajaxdatatables.html', {'data': data})



def connect_gridfs_mongodb(hostname=None, db_name=None):
    import pymongo, gridfs
    db_nameMlab = 'gridfs'
    if not hostname:
        hostname = '127.0.0.1'
        try:
            mongo = pymongo.MongoClient(hostname, waitQueueMultiple=10)
            mongo_db = mongo[db_name]
        except pymongo.errors.ConnectionFailure:
            hostname = '192.168.20.59'
            mongo = pymongo.MongoClient(hostname, waitQueueMultiple=10)
            mongo_db = mongo[db_name]
            mongo_db.authenticate('mongo', 'mongo')
    else:
        try:
            mongo = pymongo.MongoClient(hostname, waitQueueMultiple=10)
            if hostname[:7] == 'mongodb':
                db_name = hostname.split('/')[-1]
            mongo_db = mongo[db_name]
        except pymongo.errors.ConnectionFailure:
            print 'Failed --> '
            pass
    fs = ''
    fs = gridfs.GridFS(mongo_db)
    return mongo_db, fs




def mongojquery(request):
    """ Default view for the root """
    from searcher.models import *
    hostname = 'mongodb:relic7:mongo7@ds031852.mongolab.com:31852/gridfs_mrktplce'
    db_name = str(hostname.split('/'))
    mongodb_gfsmkt = connect_gridfs_mongodb(hostname=hostname, db_name=db_name)
    try:
        colorstyle = request.GET['colorstyle']
        res = mongodb_gfsmkt['fs.files'].find(colorstyle)
        #query = ProductSnapshotLive.objects.filter(colorstyle__icontains=colorstyle)
        return render(request, 'base/mongojquery.html', {'data': res})
    except:
        #data = ProductSnapshotLive.objects.all().order_by('-status_dt', '-colorstyle')[:100]
        res = mongodb_gfsmkt['fs.files'].findall().sort({"_id": "-1"})
        return render(request, 'base/mongojquery.html', {'data': res})



def unwind_metadata_array_duplicate(request):
    hostname=None
    data_src=None

    from bson import Binary, Code, SON
    if not request.get('hostname'):
        hostname = 'mongodb:relic7:mongo7@ds031852.mongolab.com:31852/gridfs_mrktplce'
    db_name = str(hostname.split('/'))

    # res = get_duplicate_records(db_name='gridfs_file7', collection_name='fs.files')
    #res = get_duplicate_records(db_name='gridfs_mrktplce', collection_name='fs.files')
    if not request.get('data_src'):
        data_src = '$metadata.File'
    if data_src[:1] == '$': pass
    else:
        data_src = str('$' + str(data_src))


    piped = [
        {"$unwind": data_src},
        {"$group": {"_id": data_src, "count": {"$sum": 1}}},
        {"$sort": SON([("count", 1), ("_id", -1)])},
        {"$limit": 55}
    ]

    mongodb_gfsmkt = connect_gridfs_mongodb(hostname=hostname, db_name=db_name)
    res = mongodb_gfsmkt['fs.files'].aggregate(piped, allowDiskUse=True)
    return render_to_response('searcher/image/image_results_v2.html', {'data': res})


def mongodisplay(request):
    """ Default view for the root """
    from searcher.models import *
    import requests, pymongo, re
    hostname = 'mongodb:relic7:mongo7@ds031852.mongolab.com:31852/gridfs_mrktplce'
    mongodb_gfsmkt = connect_gridfs_mongodb(hostname=hostname, db_name='gridfs_mrktplce')
    #mongodb_gfsmkt = connect_gridfs_mongodb(hostname=hostname, db_name=db_name)

    try:
        colorstyle = request.GET['colorstyle']
        images = mongodb_gfsmkt['fs.files'].find(colorstyle)
        return render(request, 'searcher/image/image_results_v2.html', {'images': images})
    except:
        images = mongodb_gfsmkt.fs.files.find()[:100]
        return render(request, 'searcher/image/image_results_v2.html', {'images': images})





from django.shortcuts import render_to_response
from django.template import RequestContext
from searcher.forms import testJSONForm
pmdata_url = 'http://prodimages.ny.bluefly.com/api/v1/pmdata'
localpmdata_url = 'http://localhost:9000/api/v1/pmdata'


def testjsonform(request):
    import requests,os
    try:
        #request.GET['input_list']
        colorstyle = request.GET['input_list']
    except:
        colorstyle = request.GET['data__0']
        pass
    #try:
    try:
        pmdata = requests.get(os.path.join(pmdata_url, colorstyle) + '/').json()
    except:
        pmdata = requests.get(os.path.join(localpmdata_url, colorstyle) + '/').json()
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



def reloadrefresh(request,colorstyle=None):
    import requests, json
    data=''
    try:
        colorstyle = request.GET['input_list']
        print colorstyle
        data = json.dumps({'colorstyle': colorstyle})
    except IndexError:
        pass

    res = requests.post('http://prodimages.ny.bluefly.com/images-updates', data=data)
    return res.content


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