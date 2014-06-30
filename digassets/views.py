#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.db.models import Q
from django.contrib.auth.models import User
import time
 
def index( request ):
    return render_to_response( 'index.html', {}, context_instance = RequestContext( request ) )
 