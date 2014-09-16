models.py

################################################################
#   UPLOAD Image Class Handler Model
################################################################

### file storage

from django.db import models
from django.core.files.storage import FileSystemStorage
from djdam.settings import MEDIA_ROOT

fs = FileSystemStorage(location='/media/uploads')

def get_file_path(instance, filename):
    import uuid
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('uploads/', filename)


class Product(models.Model):
    colorstyle   = models.CharField(max_length=9)
    vendor_style = models.CharField(max_length=60)
    vendor_brand = models.CharField(max_length=60)
    vendor_name =  models.CharField(max_length=60)
    #imgsource = models.CharField(max_length=70, default="internal")
    images = models.ManyToManyField(Image)
    
    class Meta:
        db_table = 'product'

    def __unicode__(self):
        return self.colorstyle


class ImageType(models.Model):
    colorstyle  = models.CharField(max_length=9)
    alt     = models.IntegerField()
    images  = models.ManyToManyField(Image)
    
    class Meta:
        db_table = 'style'

    def __unicode__(self):
        return self.alt


### file storage
from django.core.files.storage import FileSystemStorage
from djdam.settings import MEDIA_ROOT

class Image(models.Model):
    from djdam.settings import MEDIA_ROOT
    colorstyle = models.ForeignKey(Product, to_field='colorstyle', related_name='images_colorstyle')
    alt        = models.ForeignKey(ImageType, to_field='alt', related_name='images_alt')
    
    fs = FileSystemStorage(base_url='/images/', location='/media/uploads')

    uploaded_img = models.ImageField(upload_to=upload_filepath,
                              blank=True,
                              null=True,
                              height_field="height",
                              width_field="width")


    class Meta:
        db_table = 'image'
        #unique_together = ('brand', 'vendor_style',)
        #ordering = ['-colorstyle']


	def images(self):
        lst = [x.uploaded_img.name for x in self.uploaded_img.all()]
        lst = ["<a href='/media/uploads/{1}'>{0}</a>".format(x, x.split('/')[-1]) for x in lst]
        return ', '.join(lst)

    images.allow_tags = True
    def _get_absolute_url(self):
        return "/{0}/{1}/".format(MEDIA_ROOT, self.id)
#       #(Whilst this code is correct and simple, it may not be the most portable way to write this kind of method. The reverse() function is usually the best approach.)
#
#     def get_absolute_url(self):
#         from django.core.urlresolvers import reverse
#         return reverse('images.views.details', args=[str(self.id)])


