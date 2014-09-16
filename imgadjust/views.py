#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render

# Create your views here.

from models import Product, ImageType, Image
from django.shortcuts import render_to_response, get_object_or_404

def index(request):
    try:  
        colorstyle = request.get()['inputColorstyle']
    except:
        colorstyle = ''
    return render_to_response('main-display-select.html', {
        'styles': Product.objects.all().filter(colorstyle__exact=colorstyle),
        'alts'  : ImageType.objects.all().filter(colorstyle__exact=colorstyle)[:6],
        'images': Image.objects.all().filter(colorstyle__exact=colorstyle)[:6]
    })

def swap-images(request, slug):   
    return render_to_response('swap-images-confirm.html', {
        'post': get_object_or_404(Product, slug=slug)
    })

def add-replace-images(request, slug):
    Style = get_object_or_404(Product, slug=slug)
    Alt   = get_object_or_404(ImageType, slug=slug)
    return render_to_response('add-replace-images-confirm.html', {
        'Style': Style,
        'Alt': Alt,
        'image': Product.objects.filter(Style=Style).filter(Alt=Alt)[:5]
    })

def delete-images(request, slug):
    alt = get_object_or_404(ImageType, slug=slug)
    return render_to_response('delete-images-confirm.html', {
        'alt': alt,
        'styles': Product.objects.filter(alt=alt)[:5]
    })



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

