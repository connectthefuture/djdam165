#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################
__author__ = 'johnb'

from ajax_select import LookupChannel

class SongLookup(LookupChannel):

    model = Song

    def get_query(self,q,request):
        return Song.objects.filter(title__icontains=q).order_by('title')
