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

def testjsonform(request):
    json = ['a', 'b', 'c']
    form = testJSONForm(request.POST or None, initial={'data': json})
    if form.is_valid():
        # validate and save
        pass

    template = 'test_json_form.html'
    context = RequestContext(request, {'form': form})
    return render_to_response(template, context)