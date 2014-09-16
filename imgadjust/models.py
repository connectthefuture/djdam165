#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################
#   UPLOAD Image Class Handler Model
################################################################

### file storage

from django.db import models
from django.core.files.storage import FileSystemStorage
from djdam.settings import MEDIA_ROOT
import os

def get_file_path(instance, filename):
    import uuid
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('uploads/', filename)


##################################################
class Product(models.Model):
    colorstyle   = models.CharField(max_length=9)
    vendor_style = models.CharField(max_length=60)
    vendor_brand = models.CharField(max_length=60)
    vendor_name  = models.CharField(max_length=60)
    #image_source = models.CharField(max_length=70, default="internal")
    #images = models.ManyToManyField(Image)

    class Meta:
        db_table = 'product'

    def __unicode__(self):
        return self.colorstyle


##################################################
class ImageType(models.Model):
    colorstyle  = models.CharField(max_length=9)
    alt         = models.IntegerField()
    # images      = models.ManyToManyField(Image)
    
    class Meta:
        db_table = 'image_type'

    def __unicode__(self):
        return self.alt


##################################################
class ImageSource(models.Model):
    colorstyle      = models.ForeignKey(Product)
    source_url      = models.URLField(max_length=170, default="internal")
    supplier_ingest = models.ManyToManyField('searcher.SupplierIngest')
    
    class Meta:
        db_table = 'image_source'

    def __unicode__(self):
        return self.source_url    


# class Car(models.Model):
#     manufacturer = models.ForeignKey('Manufacturer')
#     # ...

# class Manufacturer(models.Model):
#     # ...
#     pass

# class Car(models.Model):
#     manufacturer = models.ForeignKey('production.Manufacturer')


##################################################
### file storage
from django.core.files.storage import FileSystemStorage
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
    colorstyle = models.ForeignKey(Product)
    source_url = models.ForeignKey(ImageSource)
    
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
        if int(self.alt) - int(1):
            return "_alt0{0}".format(str(int(self.alt) - int(1)))
        else:
            return None

    def _get_absolute_url(self):
        return "/{0}/images/{1}/{2}/{3}".format(MEDIA_ROOT, self.colorstyle, self.alt, self.image_format)

    #########################
    def _get_server_url_png(self):
        PROTOCOL = 'http'
        NETSRV101_IMAGES_ROOT = 'netsrv101.l3.bluefly.com//mnt/images/images'
        IMG_FORMAT = 'PNG'
        return "{0}://{1}/{2}/{3}{4}.{5}".format(PROTOCOL, NETSRV101_IMAGES_ROOT, self.colorstyle[:4], self.colorstyle, self.alt0, IMG_FORMAT.lower())
    server_url = property(_get_server_url_png)

#       #(Whilst this code is correct and simple, it may not be the most portable way to write this kind of method. The reverse() function is usually the best approach.)
#
#     def get_absolute_url(self):
#         from django.core.urlresolvers import reverse
#         return reverse('images.views.details', args=[str(self.id)])

    ## Image Upload Handling
    def tmpimage(self):
        from django.core.files import File
        tmp_path = '/tmp/{0}{1}_tmp'.format(self.colorstyle, self.alt0)
        f = open(tmp_path)
        tmpimage = File(f)
        return os.path.abspath(tmp_path)

    fs = FileSystemStorage(base_url='/upload/', location='{MEDIA_ROOT}uploads'.format(MEDIA_ROOT=MEDIA_ROOT))
    uploaded_image = models.ImageField(upload_to=super("Image", fs.path(tmpimage).split('/')[-1]), blank=True, null=True, height_field="height", width_field="width")

    def images(self):
        lst = [x.uploaded_image.name for x in self.uploaded_image.all()]
        lst = ["<a href='/media/uploads/{1}'>{0}</a>".format(x, x.split('/')[-1]) for x in lst]
        return ', '.join(lst)
    images.allow_tags = True


##################################################

##################################################

