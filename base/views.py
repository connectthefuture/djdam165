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
