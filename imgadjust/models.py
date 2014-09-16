#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################
#   UPLOAD Image Class Handler Model
################################################################

### file storage

from django.db import models
from django.core.files.storage import FileSystemStorage
from djdam.settings import MEDIA_ROOT

def get_file_path(instance, filename):
    import uuid
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('uploads/', filename)

class Product(models.Model):
    colorstyle   = models.CharField(max_length=9)
    vendor_style = models.CharField(max_length=60)
    vendor_brand = models.CharField(max_length=60)
    vendor_name  = models.CharField(max_length=60)
    image_source = models.URLField(max_length=170, default="internal")
    #image_source = models.CharField(max_length=70, default="internal")
    #images = models.ManyToManyField(Image)
    images      = models.ManyToManyField(Image)

    class Meta:
        db_table = 'product'

    def __unicode__(self):
        if self.image_source == 'internal': 
            return self.colorstyle
        else:
            return self.image_source

class ImageType(models.Model):
    colorstyle  = models.CharField(max_length=9)
    alt         = models.IntegerField()
    images      = models.ManyToManyField(Image)
    
    class Meta:
        db_table = 'style'

    def __unicode__(self):
        return self.alt

### file storage
from django.core.files.storage import FileSystemStorage
from djdam.settings import MEDIA_ROOT

class Image(models.Model):
    from djdam.settings import MEDIA_ROOT
    IMAGE_SIZES = (
        (u'L', u'List'),
        (u'P', u'PDP'),
        (u'Z', u'Zoom'),
    )
    IMAGE_FORMATS = (
        (u'jpg',  u'JPG'),
        (u'png',  u'PNG'),
        (u'tiff', u'TIFF'),
        (u'psd',  u'PSD'),
    )
    
    name = models.CharField(max_length=60)
    image_size = models.CharField(max_length=2, choices=IMAGE_SIZES)
    image_format = models.CharField(max_length=4, choices=IMAGE_FORMATS)
    colorstyle = models.ForeignKey(Product, to_field='colorstyle', related_name='images_colorstyle')
    source_url = models.ForeignKey(Product, to_field='image_source')
    
    class Meta:
        db_table = 'image'
        #unique_together = ('brand', 'vendor_style',)
        #ordering = ['-colorstyle']

    def get_absolute_url(self):
        #from django.core.urlresolvers import reverse
        #return reverse('people.views.details', args=[str(self.id)])
        absurl = 'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=251&height=300'.format(self.colorstyle)
        if int(self.alt) > 1:
            absalt = 'http://cdn.is.bluefly.com/mgen/Bluefly/altimage.ms?img={0}_alt0{1}.jpg&w=120&h=144'.format(self.colorstyle, str(int(self.alt) - int(1)))
            absurl = absalt
        else:
            pass
        return absurl

    def alt0(self):
        return "_alt0{0}".format(str(int(self.alt) - int(1)))

    def _get_absolute_url(self):
        return "/{0}/images/{1}/{2}/{3}".format(MEDIA_ROOT, self.colorstyle, self.alt, self.image_format)

#       #(Whilst this code is correct and simple, it may not be the most portable way to write this kind of method. The reverse() function is usually the best approach.)
#
#     def get_absolute_url(self):
#         from django.core.urlresolvers import reverse
#         return reverse('images.views.details', args=[str(self.id)])


    ## Image Upload Handling
    fs = FileSystemStorage(base_url='/upload/', location='{MEDIA_ROOT}uploads'.format(MEDIA_ROOT=MEDIA_ROOT))
    uploaded_image = models.ImageField(upload_to=upload_filepath, blank=True, null=True, height_field="height", width_field="width")

    def images(self):
        lst = [x.uploaded_image.name for x in self.uploaded_image.all()]
        lst = ["<a href='/media/uploads/{1}'>{0}</a>".format(x, x.split('/')[-1]) for x in lst]
        return ', '.join(lst)
    images.allow_tags = True

    #########################


