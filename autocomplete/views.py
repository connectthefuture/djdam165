#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.template import RequestContext
from searcher.models import ProductSnapshotLive

import django.db

def ajax_pmstyle_list(request):
    """ returns data displayed as autocomplete list - 
    this function is accessed by AJAX calls
    """
    limit = 10
    query = request.GET.get('q', None)
    # it is up to you how query looks
    if query:
        qargs = [django.db.models.Q(name__istartswith=query)]
        
    instances = ProductSnapshotLive.objects.filter(django.db.models.Q(*qargs))[:limit]

    results = ""
    for item in instances:
        results += "{0}|{1} \n".format(item.pk,item.name)

    return HttpResponse(results)
