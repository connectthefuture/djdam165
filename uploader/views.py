#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil

from django.shortcuts import render, redirect
from django.template.defaultfilters import slugify
from django.conf import settings
from django.core.files import File

from models import UploadedImage
from forms import UploadedImageForm


def image_list(request):
    images = UploadedImage.objects.all()
    return render(request, "uploader/image_list.html", {'images': images})


def image_upload(request, image_id=None):
    instance = None
    if image_id:
        instance = UploadedImage.objects.get(pk=image_id)

    if request.method == "POST":
        form = UploadedImageFormAlt(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            new_instance = form.save(commit=True)  # let's save the instance to get create its primary key

            if form.cleaned_data['delete_image'] and new_instance.image:
                new_instance.image.delete()

            if form.cleaned_data['file_path']:
                tmp_path = form.cleaned_data['file_path']
                abs_tmp_path = os.path.join(settings.MEDIA_ROOT, tmp_path)

                fname, fext = os.path.splitext(os.path.basename(tmp_path))
                filename = slugify(fname) + fext

                new_instance.image.save(filename, File(open(abs_tmp_path, "rb")), False)
                os.remove(abs_tmp_path)
            new_instance.save()
            return redirect("image_list")
    else:
        form = UploadedImageFormAlt(instance=instance)

    return render(request, "uploader/upload.html", {'instance': instance, 'form': form})

#################


from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render, redirect

from forms import UploadedImageFormAlt
from models import UploadedImage


def add_edit_image(request, uploaded_image_id=None):
    if uploaded_image_id:
        uploaded_image = get_object_or_404(UploadedImage, id=uploaded_image_id)
    else:
        uploaded_image = None

    if request.method == 'POST':
        form = UploadedImageFormAlt(instance=uploaded_image, data=request.POST, files=request.FILES)
        if form.is_valid():
            uploaded_image = form.save()
            return redirect(reverse('editadd_image', args=[uploaded_image.id]))
    else:
        form = UploadedImageFormAlt(instance=uploaded_image)

    return render(request, 'product.html', dictionary={
        'form': form,
        'uploaded_image': uploaded_image,
    })