#!/usr/bin/env python
# -*- coding: utf-8 -*-

class TastyJSONMiddleware(object):
    """
    A Django middleware to make the Tastypie API always output in JSON format
    instead of telling browsers that they haven't yet implemented text/html or
    whatever.

    WARNING: This includes a hardcoded url path for /api/.  This is not 'DRY'
    because it means you have to edit two places if you ever move your API
    path.
    """

    api_prefix = '/api/'

    def process_request(self, request):
        if request.path.startswith(self.api_prefix):
            request.META['HTTP_ACCEPT'] = 'application/json'

