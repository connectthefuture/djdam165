#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

################################################################
#   UPLOAD File Class Handler Model
################################################################

### file storage

from django.db import models
from django.core.files.storage import FileSystemStorage
from djdam.settings import MEDIA_ROOT


fs = FileSystemStorage(location='media/uploads/')

def get_file_path(instance, filename):
    import uuid
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('uploads/', filename)

################################################################

################################################################
##    FILE Model Def
################################################################

class File(models.Model):
    id = models.IntegerField(primary_key=True)
    file_path = models.FilePathField(max_length=200, unique=True)
    file_name = models.CharField(max_length=50)
    create_dt = models.DateField()
    modify_dt = models.DateTimeField(auto_now_add=True)
    ext = models.CharField(max_length=3)

    class Meta:
        db_table = 'file'
        ordering = ['-file_path']

    def __unicode__(self):
        return self.file_path

    def _get_file_type(self):
        ##"Returns the file's MIME type name."
        import urllib, os
        from urlparse import urlparse
        filetype = urlparse(self.file_path).path.split('.')[-1]
        return u'{0}'.format(filetype)
    filetype = property(_get_file_type)

    def save(self):
        return self.file_path


################################################################
#   Metadata
################################################################

class Metadata(models.Model):
    id = models.IntegerField(primary_key=True)
    file = models.ForeignKey(File)
    metadata_type = models.CharField(max_length=10,)
    metadata_tag = models.CharField(max_length=255,)
    metadata_value = models.CharField(max_length=255,)
    create_dt = models.DateField(max_length=255,)
    modify_dt = models.DateTimeField(auto_now_add=True,)
    source = models.CharField(max_length=12,)
    keywords = models.CharField(max_length=220,)
    user = models.ForeignKey(AuthUser)


    class Meta:
        #unique_together = ('file', 'metadata_type',)
        db_table = 'metadata'

    def __unicode__(self):
        return self.metadata_type


################################################################
#################### Top Level Class -- Asset #############
################################################################

class Asset(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    file_path = models.ForeignKey(File, related_name='asset_file_path', )
    metadata = models.ForeignKey(Metadata, related_name='asset_metadata')
    #tag = models.ForeignKey(Tag, related_name='asset_tag')
    #price = models.DecimalField(max_digits=5, decimal_places=2)
    asset_type = models.CharField(max_length=255)
    #photo_preview = models.ImageField(upload_to='uploads/images/preview') #,storage=fs)
    modify_dt = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(AuthUser)


#     def get_absolute_url(self):
#         return "/images/{0}/".format(self.id)
#       #(Whilst this code is correct and simple, it may not be the most portable way to write this kind of method. The reverse() function is usually the best approach.)
#
#     def get_absolute_url(self):
#         from django.core.urlresolvers import reverse
#         return reverse('images.views.details', args=[str(self.id)])


    class Meta:
        db_table = 'asset'
        ordering = ['-asset_type']

    def __unicode__(self):
        return self.file_path

    def save(self):
        return self.file_path


# ############# Admin Configs ###########

## use admin.py for config

# ############# End Admin Configs ###########

