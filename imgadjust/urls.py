#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('imgadjust.views',
    url(r'^$', 'index', name='index'),
    url(r'^swap-images/$', 'swap-images', name='swap-images'),
    url(r'^add-replace-images/$', 'add-replace-images', name='add-replace-images'),
    url(r'^delete-images/$', 'delete-images', name='delete-images'),
)

