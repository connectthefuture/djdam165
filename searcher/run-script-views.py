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
#from django.template import RequestContext

from djdam.settings import MEDIA_ROOT, MEDIA_URL
import os, sys, re, glob
# from djdam.searcher.utils.newAll_Sites_CacheClear import main as newAll_Sites_CacheClear

from .utils import newAll_Sites_CacheClear, meckPM_localLoginSave, bflyurl_scrape_return_styles_only, bfly_listpage_scrape_clear, download_server_imgs_byPOorStyleList


import time
from django.http import StreamingHttpResponse

def stream_response_generator():
    for x in range(1,11):
        yield '{} <br /> {}'.format(x, ' ' * 1024)
        time.sleep(1)

def stream_response(request):
    response = StreamingHttpResponse(stream_response_generator())
    return response

def script_runner_home_page(request):
    import subprocess
    styles = []
    script_selected = ''
    res = ''
    try:
        styles = str(request.GET['input_list'])
        print styles  
    except:
        
        try:
            if request.GET.get('input_list'):
                styles= request.GET['input_list']
                print styles
        except IndexError:        
            message = 'You submitted an empty list of styles. Please try again.'
            return HttpResponseRedirect(redirect_to='#')

    try:
        if request.GET.get('script_name'):
                script_selected = request.GET['script_name']
                print script_selected
        if script_selected == 'download_server_imgs_byPOorStyleList.py':
            if type(styles) == str and len(styles) <= 6:
                ponum = ''.join(styles)
                script_selected = os.path.join('searcher/utils', script_selected)
                # res = subprocess.call([script_selected, ponum=ponum])
                res = download_server_imgs_byPOorStyleList.main(ponum=ponum)
            else:
                if len(styles) > 9:
                    styles = ' '.join(styles)
                else:
                    styles = [styles]
                script_selected = os.path.join('searcher/utils', script_selected)
                # res = subprocess.call([script_selected, styles_list=styles])
                res = download_server_imgs_byPOorStyleList.main(styles_list=styles)

        elif script_selected == 'newAll_Sites_CacheClear.py':
            if len(styles) < 10:
                styles = list(set(str(styles).split()))
                # re.split(r'\d{9}', styles)
            else:
                styles = list(set(str(styles).split()))
                #styles = styles # ''.join(styles)
            script_selected = os.path.join('searcher/utils', script_selected)
            # res = subprocess.call([script_selected, styles_list=styles])
            res = []
            for style in styles:
                r  = style
                res.append(r)
            map(newAll_Sites_CacheClear.main, res)
        elif script_selected == 'bfly_listpage_scrape_clear.py' and len(styles) == 1:
            url = styles.pop()
            script_selected = os.path.join('searcher/utils', script_selected)
            # res = subprocess.call([script_selected, bfly_url=url])
            res = bfly_listpage_scrape_clear.main(bfly_url=[url])
        elif script_selected == 'bflyurl_scrape_return_styles_only.py' and len(styles) == 1:
            url = styles.pop()
            script_selected = os.path.join('searcher/utils', script_selected)
            # res = subprocess.call([script_selected, url])
            res = bflyurl_scrape_return_styles_only.main(bfly_url=[url])
        elif len(styles) > 1:
            for style in styles:
                if script_selected == 'meckPM_localLoginSave.py':
                    script_selected = os.path.join('searcher/utils', script_selected)
                    # res = subprocess.call([script_selected, style])
                    res = meckPM_localLoginSave.main(styles_list=styles)

        print script_selected, "SCRIPT"
    except IndexError:
        message = 'You Didnt Select a Script to run. Please try again.'
        return HttpResponseRedirect(redirect_to='/')

    if script_selected and styles:
        print 'ENTER SUBPROCSS'
        print styles, script_selected, res
        import subprocess
        ## Run the script here
        processes = []
        for style in styles:
            abs_exec_scriptpath = os.path.join('/usr/local/batchRunScripts/python', os.path.abspath(script_selected))
            processes.append(abs_exec_scriptpath)
        #results = subprocess.check_output([abs_exec_scriptpath, ' '.join(styles)]) # will then include results in return dict
        
        import multiprocessing
        pool = multiprocessing.Pool(4)
        results = pool.map(newAll_Sites_CacheClear.main,processes)
        print results
        # close the pool and wait for the work to finish
        pool.close()
        print 'PoolClose'
        pool.join()
        print 'PoolJoin'

        #return render_to_response('listing/script_output_page.html', {'styles': styles, 'script': script_selected, 'results': res}, context_instance=RequestContext(request))
        return render(request, 'listing/script_output_page.html', {'styles': styles, 'script': script_selected, 'results': results })

    else:
        message = 'Sorry, You Must have Done Something Wrong. Please check your input Data and try again.'
        return HttpResponseRedirect(redirect_to='#')
