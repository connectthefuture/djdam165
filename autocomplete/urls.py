#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('autocomplete.views',
   # ajax
   url(r'^ajax/list/$', 'ajax_pmstyle_list',
        name='ajax_pmstyle_list'),                           

)
