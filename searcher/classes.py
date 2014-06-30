#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'johnb'
## from django.conf.urls import patterns, include, url

## from apps import *
## from searcher.models import ProductSnapshotLive, ProductionRawOnfigure, ProductionRawZimages
## from searcher import views


import zipfile
from django.shortcuts import render


class ZipBuffer(object):
    """ A file-like object for zipfile.ZipFile to write into. """

    def __init__(self):
        self.data = []
        self.pos = 0

    def write(self, data):
        self.data.append(data)
        self.pos += len(data)

    def tell(self):
        # zipfile calls this so we need it
        return self.pos

    def flush(self):
        # zipfile calls this so we need it
        pass

    def get_and_clear(self):
        result = self.data
        self.data = []
        return result

def generate_zipped_stream():
    sink = ZipBuffer()
    archive = zipfile.ZipFile(sink, "w")
    for filename in ["file1.txt", "file2.txt"]:
        archive.writestr(filename, "contents of file here")
        for chunk in sink.get_and_clear():
            yield chunk


# colorstyle = ''
# brand = ''
# photo_date = ''
# outtakes = False
# styledata = ''
# found_style_data = {}
# colorstyles = []
# selects_found = ''
# selects_all = ProductionRawZimages.objects.distinct()


def photo_shoot_data_bydate(shoot_dt):
    import datetime, re
    from itertools import chain
    from searcher.models import ProductionRawZimages
    from searcher.models import ProductSnapshotLive
    from searcher.models import OnfigureSetdata
    shootdata   = OnfigureSetdata.objects.all().filter(shoot_dt__exact=shoot_dt)
    shootimages = ProductionRawZimages.objects.all().filter(photo_date__exact=shoot_dt)
    shootall = chain(shootimages,shootdata)
    return shootall, shootdata ,shootimages

from searcher.models import *
shoot_dt = ''
dayall, dayimages, shootdata=photo_shoot_data_bydate(shoot_dt)
#daydata.values('shoot_dt')
results = {}
for img in dayimages:
    results.setdefault(img.pk, []).append(img)
    for data in shootdata.filter(shoot_dt=img.photo_date):
        results[img.pk].append(data)


def photo_shoot_dataimgs_bydate(shoot_dt):
    import datetime, re
    from itertools import chain
    from searcher.models import ProductionRawZimages
    from searcher.models import ProductSnapshotLive
    from searcher.models import OnfigureSetdata

    if type(shoot_dt) == str:
        dt = datetime.datetime.strptime('2014-03-05', '%Y-%m-%d').date()

    shootdata   = OnfigureSetdata.objects.all().filter(shoot_dt__exact=shoot_dt)
    shootimages = ProductionRawZimages.objects.all().filter(photo_date__=shoot_dt)
    shootall = chain(shootimages,shootdata)

    results = {}
    for img in shootimages:
        results.setdefault(img.pk, []).append(img)
        for data in shootdata.filter(shoot_dt=img.photo_date):
            results[img.pk].append(data)
    return results


def photo_shoot_data_query(request):
    import datetime, re
    from searcher.models import Images
    from searcher.models import ProductionRawZimages
    from searcher.models import ProductSnapshotLive
    regex_date = re.compile(r'^\d{1,2}\W?\d{2}$')
    regex_datefull = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    regex_style = re.compile(r'^\d{5,9}$')
    PmData = ProductSnapshotLive.objects.all()

    images = ''
    styledata =  {}
    colorstyles = []
    selects_found = ''
    selects_all = ProductionRawZimages.objects.distinct()

    if request.POST['searchquery']:
        searchquery = request.POST['searchquery']
        if regex_datefull.findall(searchquery):
            shoot_dt = searchquery
        elif regex_style.findall(searchquery):
            colorstyle = searchquery

    results = images
    return render(request, 'image/image_results.html', { 'images': images, 'styledata': styledata})
