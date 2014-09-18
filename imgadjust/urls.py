#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('imgadjust.views',
    #    url(r'^/?.*?(?P<inputColorstyle>.+)?$', 'index', name='index'),
    #url(r'^(?P<colorstyle>\d{9})?/?(?P<alt>\d{1,5})?/?$', 'index', name='index'),
    url(r'^swap-images/$', 'swap_images', name='swap-images'),
    url(r'^add-replace-images/$', 'add_replace_images', name='add-replace-images'),
    url(r'^delete-images/$', 'delete_images', name='delete-images'),
    url(r'^.*?$', 'index', name='index2'),
    url(r'^$', 'index', name='index'),

)

