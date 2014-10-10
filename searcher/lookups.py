#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################
__author__ = 'johnb'

from ajax_select import LookupChannel
from models import ProductSnapshotLive


class ProductSnapshotLiveLookup(LookupChannel):

    model = ProductSnapshotLive

    def get_query(self,q,request):
        return ProductSnapshotLive.objects.filter(colorstyle__icontains=q).order_by('colorstyle')

