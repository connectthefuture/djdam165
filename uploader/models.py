#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _


def upload_to(instance, filename):
    if not unicode(instance.alt):
        return '/'.join(['uploads', unicode(instance.colorstyle), filename])
    else:
        return '/'.join(['uploads', unicode(instance.colorstyle), unicode(instance.alt), filename])


class UploadedImage(models.Model):
    title = models.CharField(_("Title"), max_length=200)
    image = models.ImageField(_("UploadedImage"), upload_to=upload_to, blank=True)
    # filefield = models.FileField(('main_image'), upload_to=upload_to)

    class Meta:
        verbose_name = _("UploadedImage")
        verbose_name_plural = _("UploadedImages")
        ordering = ("image",)

    def __unicode__(self):
        return self.image.path



#from django.db import models
#from app.extra import ContentTypeRestrictedFileField
#
#class upload(models.Model):
#    """ upload """
#    name = models.CharField(max_length=100)
#    description = models.CharField(max_length=250)
#    file = ContentTypeRestrictedFileField(
#        upload_to='/media/videos,'
#        content_types=['video/avi', 'video/mp4', 'video/3gp', 'video/wmp', 'video/flv', 'video/mov'],
#        max_upload_size=104857600
#    )
#    created = models.DateTimeField('created', auto_now_add=True)
#    modified = models.DateTimeField('modified', auto_now=True)
#
#    def __unicode__(self):
#        return self.name