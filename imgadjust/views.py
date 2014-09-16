#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render

# Create your views here.

from models import Product, ImageType, Image
from searcher.models import ProductSnapshotLive
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

def index(request):
    try:  
        colorstyle = str(request.GET['inputColorstyle'])
    except:
        colorstyle = '%%'
    return render_to_response('imgadjust/base/main-display-select.html', {
        #'styles': Product.objects.all().filter(product_info__colorstyle__exact=colorstyle),
        'styles': ProductSnapshotLive.objects.all().filter(colorstyle__exact=colorstyle),
        #'alts'  : ImageType.objects.all().filter(colorstyle__exact=colorstyle)[:6],
        'alts'  : ProductSnapshotLive.objects.all().filter(colorstyle__exact=colorstyle)[:6],
        'query' : colorstyle,
        'images': Image.objects.all()[:6]
    }, context_instance=RequestContext(request))

def swap_images(request, slug):
    return render_to_response('imgadjust/base/swap-images-confirm.html', {
        'post': get_object_or_404(Product, slug=slug)
    },context_instance=RequestContext(request))

def add_replace_images(request, slug):
    Style = get_object_or_404(Product, slug=slug)
    Alt   = get_object_or_404(ImageType, slug=slug)
    return render_to_response('imgadjust/base/add-replace-images-confirm.html', {
        'Style': Style,
        'Alt': Alt,
        'image': Product.objects.filter(Style=Style).filter(Alt=Alt)[:5]
    },context_instance=RequestContext(request))

def delete_images(request, slug):
    alt = get_object_or_404(ImageType, slug=slug)
    return render_to_response('imgadjust/base/delete-images-confirm.html', {
        'alt': alt,
        'styles': Product.objects.filter(alt=alt)[:5]
    },context_instance=RequestContext(request))



###################################################################################################
###############################   UploadFileWithForm   ############################################
###################################################################################################

# from django.http import HttpResponseRedirect
# from django.shortcuts import render_to_response
# from .forms import UploadFileForm
# from .models import File

# # Imaginary function to handle an uploaded file.
# from .forms import handle_uploaded_excel_file

# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             handle_uploaded_excel_file(request.FILES['file_path'])
#             #return HttpResponseRedirect('output.xls')
#             return HttpResponseRedirect(reverse('searcher.views.upload_file'))
#     else:
#         form = UploadFileForm()
#     #return render_to_response('searcher/return_download_file.html', {'form': form})
#     #return render_to_response('excel/return_download_file.html', {'form': form})
#         # Load documents for the list page
#         files = File.objects.all()

#     return render_to_response('excel/return_download_file.html',
#         {'files': files,
#          'form': form},
#         context_instance=RequestContext(request)
#     )
