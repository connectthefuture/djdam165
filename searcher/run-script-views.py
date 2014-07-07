#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'johnb'
from collections import defaultdict

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response, render
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import request, response

from djdam.settings import MEDIA_ROOT, MEDIA_URL
import os, sys

def script_runner_home_page(request):
    try:
        styles = request.POST['input_list']
    except IndexError:
        message = 'You submitted an empty list of styles please try again.'
        return HttpResponseRedirect(message=message, redirect_to='/')

    try:
        script_selected = request.POST['script_name']
    except IndexError:
        message = 'You submitted an empty list of styles please try again.'
        return HttpResponseRedirect(message=message, redirect_to='/')

    if script_selected and styles:
        import subprocess
        ## Run the script here
        # abs_exec_scriptpath = os.path.join('/usr/local/batchRunScripts/python', 'script_selected')
        # results = subprocess.check_output([abs_exec_scriptpath, styles[:]]) # will then include results in return dict

        return render(request, 'listing/script_output_page.html', {'styles': styles, 'script': script_selected, })
    else:
        message = 'Sorry, You Must have Done Something Wrong. Please check your input Data and try again.'
        return HttpResponseRedirect(message=message, redirect_to='/')