#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import *


from digassets.views import *
 
urlpatterns = patterns( '',
         url( r'^$', index, name = 'demo_index' ),
)
