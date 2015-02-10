#!/usr/bin/env python
# -*- coding: utf-8 -*-

# new
from django.db import models
import re
from tastypie.utils.timezone import now
from django.contrib.auth.models import User
from django.utils.text import slugify
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

################################################################
################################################################
##  Global Model Variables ##
#############################
#### Image Type Choice Vars as Tuples ########
ALLIMGS = '0'
PRIMARY = '1'
ALT1    = '2'
ALT2    = '3'
ALT3    = '4'
ALT4    = '5'
ALT5    = '6'

IMAGE_TYPE_CHOICES = (
    (ALLIMGS, 'AllImages'),
    (PRIMARY, 'MainImage'),
    (ALT1, 'Alt1-Back'),
    (ALT2, 'Alt2'),
    (ALT3, 'Alt3'),
    (ALT4, 'Alt4'),
    (ALT5, 'Alt5'),
)

################################################################
# from autocomplete_light import AutocompleteModel, AutocompleteTemplate
# class AutocompleteModelTemplate(AutocompleteModel, AutocompleteTemplate):
#     pass

class AdminToolsMenuBookmark(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('AuthUser')
    url = models.CharField(max_length=255L)
    title = models.CharField(max_length=255L)
    class Meta:
        db_table = 'admin_tools_menu_bookmark'

    def __unicode__(self):
        return 'Url: ' + self.url


class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=80L, unique=True)
    class Meta:
        managed = True
        db_table = 'auth_group'

    def __unicode__(self):
        return 'Group: ' + self.name


class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')
    class Meta:
        managed = True
        db_table = 'auth_group_permissions'
        verbose_name_plural = 'AuthGroupPermissions'

    def __unicode__(self):
        return 'Group: ' + str(self.id)  ##+ '\n\t' + 'Permission: ' + self.permission.codename


class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50L)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100L)
    class Meta:
        managed = True
        db_table = 'auth_permission'

    def __unicode__(self):
        #return 'CodeName: ' + self.codename + '\n\t' + 'AuthDesc: ' + self.name
        return 'AuthDesc: ' + self.name


class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=128L)
    last_login = models.DateTimeField()
    is_superuser = models.IntegerField()
    username = models.CharField(max_length=30L, unique=True)
    first_name = models.CharField(max_length=30L)
    last_name = models.CharField(max_length=30L)
    email = models.CharField(max_length=75L)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    class Meta:
        managed = True
        db_table = 'auth_user'

    def __unicode__(self):
        return 'Username: ' + self.username


class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)
    class Meta:
        managed = True
        db_table = 'auth_user_groups'
        verbose_name_plural = 'AuthUsersGroups'

    def __unicode__(self):
        return 'AuthUserID: ' + str(self.id) + ' ' + str(self.user) ##.username + '\n\t' + 'Group: ' + self.group.name


class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)
    class Meta:
        managed = True
        db_table = 'auth_user_user_permissions'

    def __unicode__(self):
        return 'AuthUserPermissionID: ' + str(self.id)  ##+ '\n\t' + 'Permission: ' + self.permission.codename


class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)
    action_time = models.DateTimeField()
    user = models.ForeignKey(AuthUser)
    content_type = models.ForeignKey('DjangoContentType', null=True, blank=True)
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=200L)
    action_flag = models.IntegerField()
    change_message = models.TextField()
    class Meta:
        db_table = 'django_admin_log'

    def __unicode__(self):
        return 'ObjectID: ' + str(self.object_id) ##+ '\n\t' + 'ContentType: ' + self.content_type.name


class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100L)
    app_label = models.CharField(max_length=100L)
    model = models.CharField(max_length=100L)
    class Meta:
        db_table = 'django_content_type'

    def __unicode__(self):
        return 'ModelName: ' + self.model + '\n\t' + 'ContentType: ' + self.name


class DjangoSession(models.Model):
    session_key = models.CharField(max_length=40L, primary_key=True)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    class Meta:
        db_table = 'django_session'

    def __unicode__(self):
        return 'SessionKey: ' + str(self.session_key) + '\n\t' + 'SessionData: ' + str(self.session_data)


class DjangoSite(models.Model):
    id = models.IntegerField(primary_key=True)
    domain = models.CharField(max_length=100L)
    name = models.CharField(max_length=50L)
    class Meta:
        db_table = 'django_site'

    def __unicode__(self):
        return 'Site: ' + self.name + '\n\t' + 'Domain: ' + self.domain


class EventsSnapshot(models.Model):
    sql_id = models.BigIntegerField(primary_key=True)
    colorstyle = models.CharField(max_length=10)
    event_id = models.CharField(max_length=7)
    event_title = models.CharField(max_length=30)
    event_group = models.CharField(max_length=30)
    event_description = models.CharField(max_length=60)
    event_detail = models.CharField(max_length=70)
    event_status = models.CharField(max_length=10)
    event_duration = models.CharField(max_length=5)
    ev_start = models.DateField()
    ev_end = models.DateField()
    product_category = models.CharField(max_length=30)
    event_type = models.CharField(max_length=30)
    event_source = models.CharField(max_length=30)
    studio_dt = models.DateField()
    jda_cat = models.CharField(max_length=30)

    class Meta:
        db_table = 'events_snapshot'

    def __unicode__(self):
        return self.event_title


class EventsStyleStatusplus(models.Model):
    sql_id = models.IntegerField(primary_key=True)
    colorstyle = models.CharField(max_length=10)
    event_id = models.CharField(max_length=7)
    event_title = models.CharField(max_length=30)
    event_group = models.CharField(max_length=30)
    event_description = models.CharField(max_length=60)
    event_detail = models.CharField(max_length=70)
    event_duration = models.CharField(max_length=3)
    ev_start = models.DateField()
    ev_end = models.DateField()
    product_category = models.CharField(max_length=30)
    production_status = models.CharField(max_length=30)
    image_dt = models.DateField()
    copy_dt = models.DateField()
    studio_dt = models.DateField()
    event_type = models.CharField(max_length=30)
    event_source = models.CharField(max_length=30)

    class Meta:
        db_table = 'events_style_statusplus'

    def __unicode__(self):
        return self.colorstyle


class OffshoreStatus(models.Model):
    id = models.IntegerField(primary_key=True)
    colorstyle = models.CharField(max_length=9L, blank=True)
    vendor_style = models.CharField(max_length=77L, blank=True)
    received_ct = models.IntegerField(null=True, blank=True)
    available_ct = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=7L, blank=True)
    category = models.CharField(max_length=13L, blank=True)
    product_type = models.CharField(max_length=21L, blank=True)
    active = models.IntegerField(null=True, blank=True)
    start_dt = models.DateField(null=True, blank=True)
    image_ready_dt = models.DateTimeField(null=True, blank=True)
    file_path_pre = models.CharField(max_length=200L, unique=True, blank=True)
    file_path_post = models.CharField(max_length=200L, unique=True, blank=True)
    modify_dt = models.DateTimeField(null=True, blank=True)
    send_dt = models.DateField(null=True, blank=True)
    return_dt = models.DateField(null=True, blank=True)
    website_url = models.URLField(max_length=200L, blank=True)

    class Meta:
        db_table = 'offshore_status'
        ordering = ['-modify_dt']
        verbose_name_plural = 'Outsourced_Clipping_Styles'
        managed = True

    #slug = models.SlugField()
    def save(self, *args, **kwargs):
        # For automatic slug generation.
        if not self.slug:
            self.slug = slugify(self.title)[:50]
        return super(OffshoreStatus, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.colorstyle

# class OffshoreZip(models.Model):
#     id = models.IntegerField(primary_key=True)
#     colorstyle = models.CharField(max_length=9L)
#     file_path_zip = models.CharField(max_length=200L, unique=True, blank=True)
#     file_path_pre = models.ForeignKey(OffshoreStatus, unique=True, null=True, db_column='file_path_pre', related_name='file_path_pre_zipfk', blank=True)
#     file_path_post = models.ForeignKey(OffshoreStatus, unique=True, null=True, db_column='file_path_post', related_name='file_path_post_zipfk', blank=True)
#     modify_dt = models.DateTimeField(null=True, blank=True)

class OffshoreZip(models.Model):
    id = models.IntegerField(primary_key=True)
    colorstyle = models.CharField(max_length=9L)
    file_path_zip = models.CharField(max_length=200L, unique=True, blank=True)
    file_path_pre = models.CharField(max_length=200L, unique=True, blank=True)
    file_path_post = models.CharField(max_length=200L, unique=True, blank=True)
    modify_dt = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'offshore_zip'
        ordering = ['-modify_dt']

    def __unicode__(self):
        return self.colorstyle

class ProductSnapshotLive(models.Model):
    sql_id = models.BigIntegerField(primary_key=True)
    colorstyle = models.CharField(max_length=9, unique=True)
    brand = models.CharField(max_length=38, blank=True)
    production_status = models.CharField(max_length=24, blank=True)
    po_number = models.CharField(max_length=8, blank=True)
    sample_status = models.CharField(max_length=38, blank=True)
    status_dt = models.DateField(null=True, blank=True)
    copy_ready_dt = models.DateField(null=True, blank=True)
    image_ready_dt = models.DateField(null=True, blank=True)
    production_complete_dt = models.DateField(null=True, blank=True)
    start_dt = models.DateField(null=True, blank=True)
    orig_start_dt = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    category = models.CharField(max_length=27, blank=True)
    product_type = models.CharField(max_length=27)
    sample_image_dt = models.DateField(null=True, blank=True)
    vendor_style = models.CharField(max_length=40)
    color = models.CharField(max_length=20)
    product_subtype = models.CharField(max_length=27, blank=True)
    sample_id = models.CharField(max_length=10, blank=True)
    sku = models.CharField(max_length=20, blank=True)
    track_number = models.CharField(max_length=38, blank=True)
    track_dt = models.DateField(null=True, blank=True)
    sample_location = models.CharField(max_length=30, blank=True)
    track_user = models.CharField(max_length=38, blank=True)
    po_type = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = 'product_snapshot_live'
        ordering = ['-colorstyle']
        verbose_name_plural = 'Production_Style_Data'
        verbose_name = 'Production_Style_Data'


    def admin_image(self):
        from django.utils.safestring import mark_safe
        # return mark_safe('<div class="effectback"><img class="effectfront" src="http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=80&height=96&ver=null"/></div>').format(self.colorstyle)
        # return mark_safe('<img style="width:50%;" src="http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=80&height=96&ver=null"/>').format(self.colorstyle)
        return mark_safe('<img src="http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=300&height=360&ver=null" onload="this.width=\'100\'; this.height=\'120\'" onmouseover="this.width=\'300\'; this.height=\'360\'" onmouseout="this.width=\'100\'; this.height=\'120\'"/>').format(self.colorstyle)
    admin_image.allow_tags = True


    def track_sample(self):
        from django.utils.safestring import mark_safe
        if str(self.track_number).isdigit() and str(self.track_number):
            fedex_url = 'http://fedex.com/Tracking?action=track&language=english&cntry_code=us&tracknumbers={0}'.format(self.track_number)
            track_url  = fedex_url
        else:
            ups_url = 'http://wwwapps.ups.com/WebTracking/track?loc=en_US&track.x=Track&trackNums={0}'.format(self.track_number)
            track_url = ups_url

        # return mark_safe('<div class="effectback"><img class="effectfront" src="http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=80&height=96&ver=null"/></div>').format(self.colorstyle)
        # return mark_safe('<img style="width:50%;" src="http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=80&height=96&ver=null"/>').format(self.colorstyle)
        return mark_safe('<a href="{0}"/>').format(track_url)
    track_sample.allow_tags = True

    def __unicode__(self):
        return self.colorstyle


class Note(models.Model):
    id = models.IntegerField(primary_key=True)
    #images = models.ManyToManyField(Images)
    note_type = models.CharField(max_length=20,)
    note_body = models.CharField(max_length=255,)
    note_date = models.DateField(max_length=12,)
    isselect = models.BooleanField(default=False)
    user = models.ForeignKey(AuthUser)


    def __unicode__(self):
        return self.note_note


    class Meta:
        #unique_together = ('images', 'note_type',)
        db_table = 'note'


class Tag(models.Model):
    id = models.IntegerField(primary_key=True)
    tag = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    #user = models.ForeignKey(User, null=True, blank=True)
    user = models.ForeignKey(AuthUser)
    value = models.CharField(max_length=50)

    def __unicode__(self):
        return self.tag  ##: self.value }

    class Meta:
        db_table = 'tag'


class Album(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=60)
    created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=50)
    public = models.BooleanField(default=True)
    notes  = models.ManyToManyField(Note)
    user = models.ForeignKey(AuthUser)
    #user = models.ForeignKey(User, null=True, blank=True)
    class Meta:
        db_table = 'album'

    def __unicode__(self):
        return self.title


    def images(self):
        lst = [x.image.name for x in self.image_set.all()]
        lst = ["<a href='/media/uploads/{0}'>{1}</a>".format(x, x.split('/')[-1]) for x in lst]
        return ', '.join(lst)
    images.allow_tags = True


######################################################################
#################### File Location Models ############################

######## File6

class SupplierIngest(models.Model):
    colorstyle = models.CharField(primary_key=True, max_length=9)
    vendor_style = models.CharField(max_length=49)
    po_number = models.CharField(max_length=7)
    version = models.CharField(max_length=10)
    vendor_name = models.CharField(max_length=70)
    vendor_brand = models.CharField(max_length=70)
    bfly_product_path = models.CharField(max_length=90)
    image_url = models.URLField(max_length=190, blank=True)
    alt = models.CharField(max_length=1, blank=True)
    image_download_valid = models.CharField(max_length=5, blank=True)
    ingest_style_id = models.CharField(max_length=10, blank=True)
    copy_ready_dt = models.DateField(blank=True, null=True)
    image_ready_dt = models.DateField(blank=True, null=True)
    production_complete_dt = models.DateField(blank=True, null=True)
    active = models.CharField(max_length=5)
    create_dt = models.DateField(blank=True, null=True)
    modified_dt = models.DateField(blank=True, null=True)
    start_dt = models.DateField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'supplier_ingest'
        ordering = ['-modified_dt', '-colorstyle', 'alt', ]
        verbose_name_plural = 'Supplier_Styles'

    @property
    def get_http_status_code(self):
        import requests
        r = requests.get(self.image_url)
        self.code = r.status_code
        return self.code

    # def get_absolute_url(self):
    #    return reversed('postready-detail', kwargs={'pk': self.pk})
    unique_together = ('colorstyle', 'alt')
    ordering = ['-colorstyle']

    def __unicode__(self):
        return self.colorstyle

    def vendor_image(self):
        from django.utils.safestring import mark_safe
        return mark_safe('<img style="width:100px;"src="{0}" onload="this.width=\'100\'; this.height=\'120\'" onmouseover="this.width=\'200\'; this.height=\'240\'" onmouseout="this.width=\'80\'; this.height=\'96\'" />').format(self.image_url)
    vendor_image.allow_tags = True

    def bfly_image(self):
        from django.utils.safestring import mark_safe
        #return mark_safe('<img src="http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=200&height=240&ver=null" onload="this.width=\'80\'; this.height=\'96\'" onmouseover="this.width=\'200\'; this.height=\'240\'" onmouseout="this.width=\'80\'; this.height=\'96\'"/>').format(self.colorstyle)
        return mark_safe('<img src="http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=100&height=120&ver={1}" alt="cached version {1}"/>').format(self.colorstyle,self.version)
    bfly_image.allow_tags = True


class SupplierIngest404(models.Model):
    colorstyle = models.CharField(primary_key=True, max_length=9)
    error_code = models.CharField(max_length=5, blank=True)
    modified_dt = models.DateTimeField(blank=True, null=True)
#    holding = models.ForeignKey(SupplierIngest,to_field=) # models.CharField(max_length=100, blank=True)

    class Meta:
        #managed = True
        db_table = 'supplier_ingest_404'

    def __unicode__(self):
        return self.file_path


class SupplierIngestImages(models.Model):
    id = models.IntegerField(primary_key=True)
    file_name = models.CharField(unique=True, max_length=20)
    colorstyle = models.CharField(max_length=9)
    vendor_style = models.CharField(max_length=55)
    po_number = models.CharField(max_length=9)
    version = models.CharField(max_length=4)
    vendor_name = models.CharField(max_length=50)
    bfly_product_path = models.CharField(max_length=100)
    image_url = models.CharField(max_length=150)
    alt = models.CharField(max_length=5)
    image_download_valid = models.CharField(max_length=5)
    ingest_style_id = models.CharField(max_length=25)
    modified_dt = models.DateField(blank=True,null=True)
    bfly_local_src = models.CharField(max_length=100, blank=True, null=True)
    bfly_zoom_src = models.CharField(max_length=150)
    bfly_zoom_site = models.CharField(max_length=150)
    bfly_list_site = models.CharField(max_length=150)
    bfly_pdp_site = models.CharField(max_length=150)


    class Meta:
        managed = False
        db_table = 'supplier_ingest_images'
        ordering = ['-colorstyle', 'alt']
        verbose_name_plural = 'Supplier_Images'

    def __unicode__(self):
        return self.file_name

    def vendor_image(self):
        from django.utils.safestring import mark_safe
        return mark_safe('<img height="96" width="80" src="{0}"/>').format(self.image_url)
    vendor_image.allow_tags = True


    def bfly_image(self):
        from django.utils.safestring import mark_safe
        if len(self.file_name) == 9:
            return mark_safe('<img src="http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=80&height=96&ver={1}"/>').format(self.colorstyle, self.version)
        else:
            return mark_safe('<img src="http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}.pct&outputx=80&outputy=96&level=1&ver={1}').format(self.file_name, self.version)
    bfly_image.allow_tags = True


class PostReadyConsignment(models.Model):
    sql_id = models.BigIntegerField(primary_key=True)
    colorstyle = models.CharField(max_length=9)
    photo_date = models.DateField()
    file_path = models.CharField(max_length=250, unique=True)
    alt = models.CharField(max_length=2)

    class Meta:
        db_table = 'post_ready_consignment'
        ordering = ['-photo_date', '-colorstyle', 'alt']

    def __unicode__(self):
        return self.file_path


class PostReadyOriginal(models.Model):
    sql_id = models.BigIntegerField(primary_key=True)
    colorstyle = models.CharField(max_length=9)
    photo_date = models.DateField()
    file_path = models.FilePathField(max_length=150, unique=True)
    alt = models.CharField(max_length=2)
    #image = models.ImageField(upload_to="images/",blank=True,null=True,height_field="height",width_field="width")

    class Meta:
        db_table = 'post_ready_original'
        ordering = ['-photo_date', '-colorstyle', 'alt']
        verbose_name_plural = 'Photography_Archived_Selects'

    def primary_select_image(self):
        from django.utils.safestring import mark_safe
        return mark_safe(
            '<img src="{0}" onload="this.width=\'80\'; this.height=\'96\'" onmouseover="this.width=\'200\'; this.height=\'240\'" onmouseout="this.width=\'80\'; this.height=\'96\'"/>').format(
            self.file_path)
        # return mark_safe('<img src="http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=80&height=96&ver=null"/>').format(self.colorstyle)
    primary_select_image.allow_tags = True

    #def get_absolute_url(self):
    #    return reversed('postready-detail', kwargs={'pk': self.pk})

    #def get_image_url(self):
    #    if self.image:
    #        return self.image.url

    def __unicode__(self):
        return self.file_path


class PushPhotoselects(models.Model):
    sql_id = models.BigIntegerField(primary_key=True)
    colorstyle = models.CharField(max_length=9)
    photo_date = models.DateField()
    file_path = models.CharField(max_length=120, unique=True)
    alt = models.CharField(max_length=2)

    def primary_select_image(self):
        from django.utils.safestring import mark_safe
        return mark_safe('<img src="{0}" onload="this.width=\'80\'; this.height=\'96\'" onmouseover="this.width=\'200\'; this.height=\'240\'" onmouseout="this.width=\'80\'; this.height=\'96\'"/>').format(self.file_path)
        # return mark_safe('<img src="http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=80&height=96&ver=null"/>').format(self.colorstyle)
    primary_select_image.allow_tags = True

    class Meta:
        db_table = 'push_photoselects'
        ordering = ['-photo_date', '-colorstyle', 'alt']
        verbose_name_plural = 'Photography_Selects'

    def __unicode__(self):
        return self.file_path


class Zimages1Photoselects(models.Model):
    sql_id = models.BigIntegerField(primary_key=True)
    colorstyle = models.CharField(max_length=9)
    photo_date = models.DateField()
    file_path = models.CharField(max_length=120, unique=True)
    alt = models.CharField(max_length=2)

    class Meta:
        db_table = 'zimages1_photoselects'
        ordering = ['-photo_date', '-colorstyle', 'alt']
        verbose_name_plural = 'Photography_ThumbSelects'

    def __unicode__(self):
        return self.file_path

    def primary_select_image(self):
        from django.utils.safestring import mark_safe
        return mark_safe(
            '<img src="{0}" onload="this.width=\'80\'; this.height=\'96\'" onmouseover="this.width=\'200\'; this.height=\'240\'" onmouseout="this.width=\'80\'; this.height=\'96\'"/>').format(
            self.file_path)
        # return mark_safe('<img src="http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=80&height=96&ver=null"/>').format(self.colorstyle)
    primary_select_image.allow_tags = True

    def _get_absolute_url(self):
        from djdam.settings import MEDIA_ROOT
        return "{0}zImages/{1}/{2}_{3}.jpg".format(
            MEDIA_ROOT,
            self.colorstyle[:4],
            self.colorstyle,
            self.alt,)
    url = property(_get_absolute_url)
#       #(Whilst this code is correct and simple, it may not be the most portable way to write this kind of method. The reverse() function is usually the best approach.)
#
#     def get_absolute_url(self):
#         from django.core.urlresolvers import reverse
#         return reverse('images.views.details', args=[str(self.id)])

    def _get_file_name(self):
        ##"Returns the file's file name without path."
        import urllib, os
        from urlparse import urlparse
        filename = urlparse(self.file_path).path.split('/')[-1]
        return u'{0}'.format(self.filename)
    filename = property(_get_file_name)


    def _get_colorstyle_name(self):
        ##"Returns the file's colorstyle,9digits name."
        import urllib, os
        from urlparse import urlparse
        filename = self.filename ##urlparse(self.file_path).path.split('/')[-1]
        return u'{0}'.format(self.filename[:9])
    #colorstyle = property(_get_colorstyle_name)


    def _get_file_type(self):
        ##"Returns the file's MIME type name."
        import urllib, os
        from urlparse import urlparse
        filetype = urlparse(self.file_path).path.split('.')[-1]
        return u'{0}'.format(filetype)
    filetype = property(_get_file_type)


class ProductionRawCp1Data(models.Model):
    id                      = models.BigIntegerField(primary_key=True)
    colorstyle              = models.CharField(max_length=9L)
    file_path                = models.CharField(max_length=245L)
    alt                     = models.CharField(max_length=1L)
    shot_number             = models.CharField(max_length=5L)
    cp1_colortag            = models.CharField(max_length=20L)
    cp1_settings_filepath   = models.CharField(max_length=260L)
    cp1_rating              = models.CharField(max_length=10L)
    cp1_other_data          = models.CharField(max_length=100L, blank=True)

    class Meta:
        db_table = 'production_raw_cp1_data'
        ordering = ['-colorstyle', 'alt', 'cp1_colortag']
        verbose_name_plural = 'Onfigure_CP1_Data'

    def __unicode__(self):
        return self.cp1_settings_filepath


class ProductionRawOnfigure(models.Model):
    sql_id                  = models.BigIntegerField(primary_key=True)
    colorstyle              = models.CharField(max_length=9)
    photo_date              = models.DateField()
    file_path               = models.CharField(max_length=200,unique=True)
    alt                     = models.CharField(max_length=2)
    shot_number             = models.CharField(max_length=6, blank=True)

    class Meta:
        db_table = 'production_raw_onfigure'
        ordering = ['-photo_date', '-colorstyle', 'alt', 'shot_number']
        verbose_name_plural = 'Onfigure_Outakes'

    def primary_select_image(self):
        from django.utils.safestring import mark_safe

        return mark_safe(
            '<img src="{0}" onload="this.width=\'80\'; this.height=\'96\'" onmouseover="this.width=\'200\'; this.height=\'240\'" onmouseout="this.width=\'80\'; this.height=\'96\'"/>').format(
            self.file_path)
        # return mark_safe('<img src="http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=80&height=96&ver=null"/>').format(self.colorstyle)
    primary_select_image.allow_tags = True

    def __unicode__(self):
        return self.file_path


class ProductionRawZimages(models.Model):
    sql_id                  = models.BigIntegerField(primary_key=True)
    colorstyle              = models.CharField(max_length=9, blank=True)
    photo_date              = models.DateField(null=True, blank=True)
    file_path               = models.CharField(max_length=250, unique=True)
    alt                     = models.CharField(max_length=2)
    shot_number             = models.CharField(max_length=6, blank=True)

    class Meta:
        db_table = 'production_raw_zimages'
        ordering = ['-photo_date', '-colorstyle', 'alt', 'shot_number']
        verbose_name_plural = 'Onfigure_ThumbOutakes'

    def __unicode__(self):
        return self.file_path

    from djdam.settings import MEDIA_ROOT
    def _get_absolute_url(self):

        return "/{0}/studio_thumbs/{1}/{2}_{3}_{4}_CR2.jpg".format(MEDIA_ROOT,
            self.colorstyle[:4],
            self.colorstyle,
            self.alt,
            self.shot_number,)
    url = property(_get_absolute_url)

######## NetSrv101

# class SiteImagesFileBfly(models.Model):
# #    selects_id = models.IntegerField(maxlength=15, blank=True, null=True)

#     sql_id = models.BigIntegerField(primary_key=True)
#     colorstyle = models.CharField(max_length=9)
#     photo_date = models.DateField()
#     file_path = models.CharField(max_length=150,unique=True)
#     urlfield = models.URLField(max_length=150,unique=True)
#     alt = models.CharField(max_length=2)

# #    shot_number = models.CharField(max_length=6)
# #    metadata = models.CharField(maxlength=200)
# #    filetype = models.CharField(maxlength=20)

#     class Meta:
#         db_table = 'site_images_bluefly'
#         ordering = ['-photo_date', '-colorstyle', 'alt']

    # def __unicode__(self):
    #     return self.url

    # def _get_file_name(self):
    #     ##"Returns the file's file name without path."
    #     import urllib, os
    #     from urlparse import urlparse
    #     filename = urlparse(self.url).path.split('/')[-1]
    #     return u'{0}'.format(self.filename)
    # filename = property(_get_file_name)

    # def _get_colorstyle_name(self):
    #     ##"Returns the file's colorstyle,9digits name."
    #     import urllib, os
    #     from urlparse import urlparse
    #     filename = self.filename ##urlparse(self.file_path).path.split('/')[-1]

    #     return u'{0}'.format(self.filename[:9])
    # colorstyle = property(_get_colorstyle_name)


    # from settings import MEDIA_ROOT
    # PROTOCOL = 'http'
    # NETSRV101_IMAGES_ROOT = 'netsrv101.l3.bluefly.com//mnt/images/images'

    # def _get_absolute_url(self):

    #     return "{0}://{1}/{2}/{3}/".format(PROTOCOL, NETSRV101_IMAGES_ROOT, colorstyle[:4], filename)
    # url = property(_get_absolute_url)
#       #(Whilst this code is correct and simple, it may not be the most portable way to write this kind of method. The reverse() function is usually the best approach.)
#
#     def get_absolute_url(self):
#         from django.core.urlresolvers import reverse
#         return reverse('images.views.details', args=[str(self.id)])



# class SiteImagesFileBclv(models.Model):
# #    selects_id = models.IntegerField(maxlength=15, blank=True, null=True)

#     sql_id = models.BigIntegerField(primary_key=True)
#     colorstyle = models.CharField(max_length=9)
#     photo_date = models.DateField()
#     file_path = models.CharField(max_length=150,unique=True)
#     alt = models.CharField(max_length=2)

# #    shot_number = models.CharField(max_length=6)
# #    metadata = models.CharField(maxlength=200)
# #    filetype = models.CharField(maxlength=20)

#     class Meta:
#         db_table = 'site_images_belleclive'
#         ordering = ['-photo_date', '-colorstyle', 'alt']

#     def __unicode__(self):
#         return self.file_path




############# End File Location Models ####


class Vendor(models.Model):
    id = models.AutoField(primary_key=True)
    vendor_name = models.ManyToManyField(SupplierIngest)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    #merchant = models.ForeignKey(Merchant)
    website = models.URLField(max_length=150, blank=True, null=True)
    #imgisstd = models.Boolean(Merchant)
    ftpurl_prefix = models.URLField(max_length=150, blank=True, null=True)
    class Meta:
        db_table = 'vendor'

    def __unicode__(self):
        return self.vendor_name


class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    brand = models.ManyToManyField(ProductSnapshotLive, related_name='snp_brand')
    departments = models.CharField(max_length=50, blank=True, null=True)
    brandtype = models.CharField(max_length=50, blank=True, null=True)
    #vendors = models.ManyToManyField(Vendor)
    class Meta:
        db_table = 'brand'
        #ordering = ['departments','name']

    def __unicode__(self):
        return u'%s' % (self.brand)



class Color(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.OneToOneField('ProductSnapshotLive', related_name='snp_color') ## , to_field='color')

    class Meta:
        db_table = 'color'
        #ordering = ['name']

    def __unicode__(self):
        return self.name



class Event(models.Model):
    id = models.IntegerField(primary_key=True)
    event_id = models.IntegerField(max_length=15)
    ev_start = models.DateField()
    ev_end = models.DateField()
    event_title = models.CharField(max_length=200, unique=True)
    editorial_styles = models.CharField(max_length=60)
    categoryid = models.CharField(max_length=15)

    class Meta:
        db_table = 'event'
        ordering = ['-event_id']

    def __unicode__(self):
        return self.event_id


class Images(models.Model):
#   #pmdata = models.ForeignKey(ProductSnapshotLive)
#   #metadata = models.CharField(max_length=200)
#   #vendor_style = models.CharField(max_length=50)
#   #product = models.ForeignKey(ProductionRawZimages)
# #    image_outtake = models.ForeignKey(OuttakeImageFileHres)
# #    image_outtake_thumb = models.ForeignKey(OuttakeImageFileZres)
# #    image_outtake_push = models.ForeignKey(OuttakeImageFilePush)
# #    image_select = models.ForeignKey(SelectImageFileHres)
# #    image_select_thumb = models.ForeignKey(SelectImageFileZres)
# #    image_select_push = models.ForeignKey(SelectImageFilePush)
# #    image_vendor_bclv = models.ForeignKey(ConsigImageFileBclv)
# #    image_vendor_bfly = models.ForeignKey(ConsigImageFileBfly)
# #    image_site_bclv = models.ForeignKey(SiteImageFileBclv)
# #    image_site_bfly = models.ForeignKey(SiteImageFileBfly)

    from djdam.settings import MEDIA_ROOT


    id = models.AutoField(primary_key=True)
    colorstyle = models.ForeignKey(ProductSnapshotLive, to_field='colorstyle', related_name='images_colorstyle')

    image_outtake       = models.ForeignKey(ProductionRawZimages, related_name='outtake', to_field='file_path')
    image_select        = models.ForeignKey(PostReadyOriginal, related_name='select', to_field='file_path')
    image_select_thumb  = models.ForeignKey(Zimages1Photoselects, related_name='select_thumb', to_field='file_path')
    image_select_push   = models.ForeignKey(PushPhotoselects, related_name='select_push', to_field='file_path')


    #groups = groups.objects.filter(item__in=items).distinct().values_list('name', flat=True)
    #CC.objects.filter( bb__aa = aa_instance )
    ### file storage
    from django.core.files.storage import FileSystemStorage
    from djdam.settings import MEDIA_ROOT

    #upload_filepath  = str("images/" + str("{0}_{1}.png".format(colorstyle, id)))
    #upload_mediaurul = str("/images/" + str("{0}_{1}.png".format(colorstyle, id)))

    fs = FileSystemStorage(base_url='/images/', location='/media/uploads')

    # image = models.ImageField(upload_to=upload_filepath,
    #                           blank=True,
    #                           null=True,
    #                           height_field="height",
    #                           width_field="width")

    class Meta:
        db_table = 'images'
        #unique_together = ('brand', 'vendor_style',)
        #ordering = ['-colorstyle']
        verbose_name_plural = 'Image_BaseModel'


    def _get_absolute_url(self):
        return "/{0}/{1}/".format(MEDIA_ROOT, self.id)
        # (Whilst this code is correct and simple, it may not be the most portable way to write this kind of method.
        # The reverse() function is usually the best approach.)
        #
        #     def get_absolute_url(self):
        #         from django.core.urlresolvers import reverse
#         return reverse('images.views.details', args=[str(self.id)])


    def _get_file_name(self):
        ##"Returns the file's file name without path."
        import urllib, os
        from urlparse import urlparse
        filename = urlparse(self.file_path).path.split('/')[-1]
        return u'{0}'.format(self.filename)
    filename = property(_get_file_name)


    def _get_colorstyle_number(self):
        ##"Returns the file's colorstyle,9digits name."
        import urllib, os
        from urlparse import urlparse
        colorstyle = urlparse(self.file_path).path.split('/')[-1][:9]
        return u'{0}'.format(colorstyle)
    colorstyle_from_file = property(_get_colorstyle_number)


    def _get_alt_number(self):
        ##"Returns the file's Alt image reference number."
        import urllib, os
        from urlparse import urlparse
        alt = urlparse(self.file_path).path.split('/')[-1][11]
        return u'{0}'.format(alt)
    alt = property(_get_alt_number)


    def _get_shot_number(self):
        ##"Returns the file's shot number if included in file_path."
        import urllib, os
        from urlparse import urlparse
        shot_number = urlparse(self.file_path).path.split('/')[-1][12:].split('.')[1]
        return u'{0}'.format(shot_number)
    shot_number = property(_get_shot_number)


    def _get_file_type(self):
        ##"Returns the file's MIME type name."
        import urllib, os
        from urlparse import urlparse
        filetype = urlparse(self.file_path).path.split('.')[-1]
        return u'{0}'.format(filetype)
    filetype = property(_get_file_type)


    def save(self, *args, **kwargs):
        # For automatic slug generation.
        # if not self.slug:
        #    self.slug = slugify('%d') % self.timestamp
        return super(Images, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.colorstyle



# class ScriptRunner(models.Model):
#     name    = models.CharField(max_length=40)
#     file_path = models.FilePathField(max_length=240)
#     params    = models.CharField(max_length=100)


class SelectedFiles(models.Model):
    id = models.IntegerField(primary_key=True)
    user    = models.ForeignKey(User)
    source_pk  = models.CharField(max_length=10)
    file_path  = models.FilePathField(max_length=240)
    #file_path = models.ForeignKey('Images', to_field='id')
    #upload_to='selected/%Y/%m/%d'
    ipaddress  = models.IPAddressField(max_length=17)#models.ForeignKey('AuthUser')
    #user_id    = models.IntegerField(max_length=11)#models.ForeignKey('AuthUser')
    session_id = models.CharField(max_length=40)#models.ForeignKey('DjangoSession', to_field='session_key')
    create_dt = models.DateField()
    rating = models.IntegerField(null=True, blank=True)
    notes = models.CharField(max_length=200L, blank=True)
    modify_dt = models.DateTimeField(default=now)
    ##null=True, blank=True)
    #    colorstyle = models.CharField(max_length=255)

    slug = models.SlugField()
    def save(self, *args, **kwargs):
        # For automatic slug generation.
        if not self.slug:
            self.slug = slugify(self.title)[:50]
        return super(SelectedFiles, self).save(*args, **kwargs)

    class Meta:
        db_table = 'selected_files'
        ordering = ['-create_dt', '-file_path']
        verbose_name_plural = 'Selected_DAM_Files'

    def __unicode__(self):
        return self.file_path

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    colorstyle = models.ForeignKey(ProductSnapshotLive, to_field='colorstyle', related_name='snp_colorstyle')
    #brand = models.ForeignKey(ProductSnapshotLive, to_field='brand', related_name='snp_brand')
    #color = models.ForeignKey(ProductSnapshotLive, to_field='color', related_name='snp_color')
    # vendor = models.ForeignKey('Vendor')
    # brand = models.ForeignKey('Brand')
    # color = models.ForeignKey('Color')
    #events     = models.ManyToManyField(Event)
    images     = models.ManyToManyField(Images)
    #gender = models.CharField(max_length=20)
    #product_type = models.CharField(max_length=50)
    #pmdata = models.ForeignKey(ProductSnapshotLive)
    #metadata = models.CharField(max_length=200)
    #vendor_style = models.CharField(max_length=50)
    #photo_date = models.ForeignKey(Zimages1Photoselects, to_field='photo_date', related_name='prod_photodate')
    primary_zimage  = models.FilePathField(Zimages1Photoselects)
    image_preview   = models.ImageField(upload_to="images/",
                              blank=True,
                              null=True,
                              height_field="height",
                              width_field="width")
    class Meta:
        managed = True
        db_table = 'product'
        #unique_together = ('brand', 'vendor_style',)
        #ordering = ['-colorstyle']

    def save(self, *args, **kwargs):
        # For automatic slug generation.
        # if not self.slug:
        #    self.slug = slugify('%d') % self.timestamp
        return super(Product, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.colorstyle


class ImageUpdate(models.Model):
    #snapshotdata = models.ForeignKey('ProductSnapshotLive')
    colorstyle = models.CharField(max_length=9)
    alt = models.CharField(max_length=3, default="1")#, blank=True)
    create_dt   = models.DateTimeField(auto_now_add=True)
    modify_dt   = models.DateTimeField(auto_now=True)
    image_type  = models.CharField(max_length=3,
                                  choices=IMAGE_TYPE_CHOICES,
                                  default=PRIMARY)
    cache_cleared = models.BooleanField(False, blank=True)
    updated_by = models.CharField(max_length=15)
    ## below param on updated by seemed unnecessary for now
    #models.ForeignKey(AuthUser, null=True, blank=True, to_field='username', related_name='image_update_user')
    #deleted_by = models.ForeignKey('auth.User', null=True, related_name='profile_user_deleted')
    class Meta:
        managed = True
        db_table = 'image_update'
        unique_together = ('colorstyle', 'alt',)
        ordering = ['-modify_dt', 'colorstyle', 'alt']
        verbose_name_plural = 'Image_Cache_Updates'

    def save(self, *args, **kwargs):
        # For automatic slug generation.
        # if not self.slug:
        #    self.slug = slugify('%d') % self.timestamp
        return super(ImageUpdate, self).save(*args, **kwargs)

    def __unicode__(self):
        if self.alt == '1':
            alt= 'Primary'
        else:
            alt = self.alt
        return "Style {0} \nImage Type: {1}".format(self.colorstyle, self.alt)


    def count_styles_images(self):
        count = self.image_type in (self.ALT1, self.ALT2, self.ALT3, self.ALT4, self.ALT5 )
        return len(count + 1)


####################

from djdam.settings import MEDIA_ROOT
import os
class LocalImageURL(models.Model):
    upload_path = os.path.join(MEDIA_ROOT, 'images')
    image = models.ImageField(upload_to='uploads/images/', null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
            db_table = 'local_image_URL'
            #unique_together = ('image_url', 'image',)
            #ordering = ['-colorstyle']


    def save(self, *args, **kwargs):
        if self.image_url:
            import urllib, os
            from urlparse import urlparse
            filename = urlparse(self.image_url).path.split('/')[-1]

            ## make dir struct if not already created, else skip
            upload_path = os.path.join(MEDIA_ROOT, 'images')
            file_save_dir = os.path.join(upload_path, str(filename[:4]), str(filename[:9]))
            if not os.path.isdir(file_save_dir):
                os.makedirs(file_save_dir)

            urllib.urlretrieve(self.image_url, os.path.join(file_save_dir, filename))
            self.image = os.path.join(file_save_dir, filename)
            self.image_url = ''
        super(LocalImageURL, self).save()


    def _get_filename(self):
        "Returns the urls's filename,9digits name."
        return u'{0}'.format((self.image_url).path.split('/')[-1])
    filename = property(_get_filename)


    def __unicode__(self):
        return self.image_url



####################
# ... Brand and Vendor models must be before manager ...
## Count of styles by brand

# class ProductVendorManager(models.Manager):
#     def colorstyle_count(self, brandname):
#         return self.filter(brand.name__icontains=brandname).count()

# class ProductVendor(models.Model):
#     colorstyle = models.CharField(max_length=100)
#     vendorstyle = models.CharField(max_length=100)
#     brand = models.ForeignKey(Brand)
#     vendor = models.ForeignKey(Vendor)
#     #publication_date = models.DateField()
#     num_pages = models.IntegerField(blank=True, null=True)
#     #objects = ProductVendorManager()
#     class Meta:
#         db_table = 'product_vendor'

#     def __unicode__(self):
#         return self.colorstyle


# class ImageBase(models.Model):
#     colorstyle = models.CharField(max_length=9)
#     photo_date = models.DateField()
#     file_path = models.FilePathField(max_length=150, unique=True)
#     alt = models.CharField(max_length=2)
#     upload_image = models.ImageField(upload_to="images/",
#                                      blank=True,
#                                      null=True,
#                                      height_field="height",
#                                      width_field="width")
#     class Meta:
#         abstract = True


class OnfigureSetdata(models.Model):
    id = models.IntegerField(primary_key=True)
    shoot_dt = models.DateField(unique=True)
    location = models.CharField(max_length=8L, blank=True)
    uid = models.CharField(max_length=41L, blank=True)
    modify_dt = models.CharField(max_length=16L, blank=True)
    photographer = models.CharField(max_length=11L, blank=True)
    digital_tech = models.CharField(max_length=12L, blank=True)
    merch = models.CharField(max_length=15L, blank=True)
    makeup_grooming = models.CharField(max_length=17L, blank=True)
    stylist = models.CharField(max_length=17L, blank=True)
    model = models.CharField(max_length=20L, blank=True)
    agency = models.CharField(max_length=10L, blank=True)
    summary = models.CharField(max_length=15L, blank=True)
    session_notes = models.CharField(max_length=87L, blank=True)

    def __unicode__(self):
        return self.summary

    class Meta:
        db_table = 'onfigure_setdata'
        #ordering = ['-shoot_dt']
        #unique_together = ['shoot_dt', 'location']
        verbose_name_plural = 'Onfigure_Set_Data'


class Photo_Shoot(models.Model):
    id = models.IntegerField(primary_key=True)
    images = models.ManyToManyField(ProductionRawZimages)
    shoot_date = models.ForeignKey(OnfigureSetdata,
                                   to_field='shoot_dt',
                                   related_name='onfigure_images')

    def __unicode__(self):
        return self.shoot_date

    class Meta:
        db_table = 'photo_shoot'
        ordering = ['-id']


class ExcelToolData(models.Model):
    id = models.BigIntegerField(primary_key=True)
    colorstyle = models.CharField(max_length=9, unique=True)
    po_number = models.CharField(max_length=8)
    vendor_style = models.CharField(max_length=40)
    material = models.CharField(max_length=70)
    bullet_1 = models.CharField(max_length=90, blank=True)
    bullet_2 = models.CharField(max_length=90, blank=True)
    bullet_3 = models.CharField(max_length=90, blank=True)
    bullet_4 = models.CharField(max_length=90, blank=True)
    bullet_5 = models.CharField(max_length=90, blank=True)
    bullet_6 = models.CharField(max_length=90, blank=True)
    bullet_7 = models.CharField(max_length=90, blank=True)
    bullet_8 = models.CharField(max_length=90, blank=True)
    bullet_9 = models.CharField(max_length=90, blank=True)
    short_name = models.CharField(max_length=90, blank=True)
    long_description = models.CharField(max_length=220, blank=True)
    country_origin = models.CharField(max_length=3, blank=True)
    return_policy_id = models.CharField(max_length=10, blank=True)
    copy_ready_dt = models.DateField(null=True, blank=True)
    care_instructions_id = models.CharField(max_length=10, blank=True)
    color_group_id = models.CharField(max_length=5, blank=True)

    class Meta:
        db_table = 'excel_tool_data'
        ordering = ['-colorstyle']
        verbose_name_plural = 'Required_Copy_Data'

    def __unicode__(self):
        return self.colorstyle


class ViewExcelToolDuplicateVendorStyle(models.Model):
    colorstyle = models.CharField(unique=True, max_length=9L)
    vendor_style = models.CharField(max_length=40L)
    po_number = models.CharField(max_length=8L)
    color_group_id = models.CharField(max_length=5L, blank=True)
    count = models.BigIntegerField()
    class Meta:
        db_table = 'view_excel_tool_duplicate_vendor_style'
        ordering = ['vendor_style','color_group_id', 'colorstyle']

####################################

class File(models.Model):
    id = models.AutoField(primary_key=True)
    #colorstyle = models.ForeignKey(Product)
    #images = models.ManyToManyField('SearcherProductImages', related_name='product_images')
    file = models.FileField("File", upload_to='uploads/%Y/%m/%d')
    file_path = models.FilePathField(max_length=200, unique=True)
    file_name = models.CharField(max_length=50)
    create_dt = models.DateTimeField(blank=True)
    modify_dt = models.DateTimeField(blank=True)
    ext = models.CharField(max_length=3)

    class Meta:
        db_table = 'file'
        ordering = ['-file_path']


    @property
    def _get_file_url(self):
        # #"Returns the file's MIME type name."
        import urllib, os
        from urlparse import urlparse
        url = urlparse(self.file)
        return u'{0}'.format(url)
    url = property(_get_file_url)


    @property
    def _get_file_name(self):
        # #"Returns the file's MIME type name."
        import urllib, os
        from urlparse import urlparse
        name = urlparse(self.file).split('/')[-1].split('.')[0]
        return u'{0}'.format(name)
    name = property(_get_file_name)


    @property
    def _get_file_type(self):
        # #"Returns the file's MIME type name."
        import urllib, os
        from urlparse import urlparse
        filetype = urlparse(self.file).split('/')[-1].split('.')[-1]
        return u'{0}'.format(filetype)
    filetype = property(_get_file_type)

    def save(self, *args, **kwargs):
        # For automatic slug generation.
        # if not self.slug:
        #    self.slug = slugify('%d') % self.timestamp
        return super(File, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.file_path


class Document(models.Model):
    docfile = models.FileField(upload_to='uploads/%Y/%m/%d')

    def save(self, *args, **kwargs):
        # For automatic slug generation.
        # if not self.slug:
        #    self.slug = slugify('%d') % self.timestamp
        return super(Document, self).save(*args, **kwargs)

################################################################
#   Metadata
################################################################

class Metadata(models.Model):
    id = models.AutoField(primary_key=True)
    #images = models.ManyToManyField(Images)
    #file = models.ForeignKey(File)
    metadata_type = models.CharField(max_length=10,)
    metadata_tag = models.CharField(max_length=255,)
    metadata_value = models.CharField(max_length=255,)
    create_dt = models.DateField(max_length=255,)
    modify_dt = models.DateTimeField(auto_now_add=True,)
    source = models.CharField(max_length=12,)
    keywords = models.CharField(max_length=220,)
    user = models.ForeignKey(AuthUser)
    #position = models.PositiveSmallIntegerField("Position")

    class Meta:
        managed = True
        #unique_together = ('image', 'metadata_type',)
        db_table = 'metadata'
        #ordering = ('position',)
        verbose_name_plural = 'Metadata'

    def save(self, *args, **kwargs):
        # For automatic slug generation.
        # if not self.slug:
        #    self.slug = slugify('%d') % self.timestamp
        return super(Metadata, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.metadata_type

#################### Top Level Class -- Asset #############

class Asset(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    file_path = models.ForeignKey(File, related_name='asset_file_path')
    metadata = models.ForeignKey(Metadata, related_name='asset_metadata')
    tag = models.ForeignKey(Tag, related_name='asset_tag')
    #price = models.DecimalField(max_digits=5, decimal_places=2)
    asset_type = models.CharField(max_length=255)
    #photo_preview = models.ImageField(upload_to='uploads/images/preview') #,storage=fs)
    modify_dt = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(AuthUser)

#     def get_absolute_url(self):
#         return "/images/{0}/".format(self.id)
# 		#(Whilst this code is correct and simple, it may not be the most portable way to write this kind of method. The reverse() function is usually the best approach.)
#
#     def get_absolute_url(self):
#         from django.core.urlresolvers import reverse
#         return reverse('images.views.details', args=[str(self.id)])

    class Meta:
        managed = True
        db_table = 'asset'
        ordering = ['-asset_type']

    def __unicode__(self):
        return self.file_path

    def save(self, *args, **kwargs):
        # For automatic slug generation.
        # if not self.slug:
        #    self.slug = slugify('%d') % self.timestamp
        return super(Asset, self).save(*args, **kwargs)

##############################################################################
##############################################################################
################ Looklet file and reporting handling Models###################
##############################################################################

class LookletMetadataSidecar(models.Model):
    id = models.AutoField(primary_key=True)  # AutoField?
    metadata_type = models.CharField(max_length=10)
    metadata_tag = models.CharField(max_length=255)
    metadata_value = models.CharField(max_length=255)
    create_dt = models.DateField()
    modify_dt = models.DateTimeField()
    source = models.CharField(max_length=12)
    keywords = models.CharField(max_length=220)
    user_id = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'looklet_metadata_sidecar'
        ordering = ['-create_dt', '-modify_dt']
        verbose_name_plural = 'Looklet_Metadata'

    def __unicode__(self):
        return self.metadata_value

    def save(self, *args, **kwargs):
        # For automatic slug generation.
        # if not self.slug:
        #    self.slug = slugify('%d') % self.timestamp
        return super(LookletMetadataSidecar, self).save(*args, **kwargs)

# class LookletShotListPostReadyOriginal(models.Model):
#     #id = models.BigIntegerField(primary_key=True)
#     colorstyle = models.ForeignKey('LookletShotList',  related_name='looklet_colorstyles_sent')
#     file_paths = models.ManyToManyField('PostReadyOriginal', related_name='looklet_file_paths_returned+')
#
#     class Meta:
#         managed = True
#         ordering = ['-colorstyle', '-file_paths']
#         verbose_name_plural = 'Looklet_PostReady_M2M'
#
#     def __unicode__(self):
#         return self.file_paths

# class LookletReturned(models.Model):
#     id = models.BigIntegerField(primary_key=True)
#     #capture_date = models.ForeignKey('LookletShotList', to_field='photo_date')
#     colorstyle = models.ForeignKey('LookletShotList')
#     file_paths = models.ManyToManyField(PostReadyOriginal, related_name='looklet_file_paths_returned+') ##, through='LookletShotListPostReadyOriginal', through_fields=('file_paths','colorstyle'))
#     metadata = models.ManyToManyField(LookletMetadataSidecar)
#
#     class Meta:
#         managed = True
#         #ordering = ['-colorstyle']
#         verbose_name_plural = 'Looklet_Returned_Files'
#
    # def save(self, *args, **kwargs):
    #     # For automatic slug generation.
    #     # if not self.slug:
    #     #    self.slug = slugify('%d') % self.timestamp
    #     return super(LookletReturned, self).save(*args, **kwargs)
#     def __unicode__(self):
#         return self.file_path

class LookletShotList(models.Model):
    id = models.AutoField(primary_key=True)
    colorstyle = models.CharField(max_length=9)
    photodate = models.DateField(max_length=10, blank=True, null=True)
    reshoot = models.CharField(max_length=1, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(unique=True)
    username = models.CharField(max_length=75, blank=True, null=True)


    class Meta:
        managed = True
        db_table = 'looklet_shot_list'
        #ordering = ['-timestamp', '-colorstyle' ]
        verbose_name_plural = 'Looklet_ShotLists'
        #unique_together = ['colorstyle', 'photodate']

    #hash = models.CharField(primary_key=True, max_length=32)

    #def create_hash(self):
    #    return os.urandom(32).encode('hex')


    #slug = models.SlugField(blank=True,null=True)
    def save(self, *args, **kwargs):
        #For automatic slug generation.
        # if not self.slug:
        #    self.slug = slugify('%s') % self.id
        return super(LookletShotList, self).save(*args, **kwargs)


    def __unicode__(self):
        return '{0}_{1}'.format(self.colorstyle,self.photodate[:10])


    def primary_select_small(self):
        from django.utils.safestring import mark_safe
        img_url = "{0}zImages/{1}/{2}_1.jpg".format(MEDIA_ROOT, self.colorstyle[:4], self.colorstyle)
        return mark_safe('<img href="#" class="img-rounded" style="width: 120px;" src="{0}"  alt="{1}"/>').format(img_url, self.timestamp)
        #return mark_safe(
        #    '<img src="{0}" onload="this.width=\'80\'; this.height=\'96\'" onmouseover="this.width=\'200\'; this.height=\'240\'" onmouseout="this.width=\'80\'; this.height=\'96\'"/>').format(self.file_path)
    primary_select_small.allow_tags = True


    def primary_select_zthumb(self):
        #from djdam.settings import MEDIA_URL
        zroot='http://192.168.20.242/'
        zroot='http://192.168.20.242/'
        img_url = "{0}zImages_1/{1}/{2}_1.jpg".format(zroot, self.colorstyle[:4], self.colorstyle)
        from django.utils.safestring import mark_safe
        return mark_safe('<img href="#" class="img-rounded" style="width: 240px;" src="{0}"  alt="{1}"/>').format(img_url, self.timestamp)
    #primary_select_thumb = property(primary_select_zthumb)
    primary_select_zthumb.allow_tags = True

    def back_select_zthumb(self):
        #from djdam.settings import MEDIA_ROOT
        zroot='192.168.20.242/'
        img_url = "{0}zImages/{1}/{2}_2.jpg".format(zroot, self.colorstyle[:4], self.colorstyle)
        from django.utils.safestring import mark_safe
        return mark_safe('<img href="#" class="img-rounded" style="width: 240px;" src="{0}" alt="{1}"/>').format(img_url, self.timestamp)
    back_select_thumb = property(back_select_zthumb)


    def primary_pdp_image(self):
        from django.utils.safestring import mark_safe
        return mark_safe('<img href="/reloadrefresh/{0}" src="http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=340&height=408&ver=null" class="img-rounded" style="width: 240px;"/>').format(self.colorstyle)
    primary_pdp_image.allow_tags = True


    def bfly_list_image(self):
        from django.utils.safestring import mark_safe
        ##if len(self.file_name) == 9:
        return mark_safe('<img href="#" src="http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=250&height=301&ver=null" class="img-rounded" style="width: 240px;"/>').format(self.colorstyle)
    bfly_list_image.allow_tags = True


##############################################################################
### Mongo DB Models ###
#######################


##############################################################################
##############################################################################
##############################################################################

# class OnfigureSetdataImages(models.Model):
#     id = models.IntegerField(primary_key=True)
#     shoot_dt = models.DateField()
#     photographer = models.ForeignKey(OnfigureSetdata)
#     digital_tech = models.ForeignKey(OnfigureSetdata)
#     merch = models.ForeignKey(OnfigureSetdata)
#     makeup_grooming = models.ForeignKey(OnfigureSetdata)
#     stylist = models.ForeignKey(OnfigureSetdata)
#     model = models.ForeignKey(OnfigureSetdata)
#     agency = models.ForeignKey(OnfigureSetdata)
#     summary = models.ForeignKey(OnfigureSetdata)
#     images = models.ManyToManyField(ProductionRawZimages,)
    # image_outtake       = models.ForeignKey(ProductionRawZimages, related_name='outtake', to_field='file_path')
    # image_select        = models.ForeignKey(PostReadyOriginal, related_name='select', to_field='file_path')
    # image_select_thumb  = models.ForeignKey(Zimages1Photoselects, related_name='select_thumb', to_field='file_path')
    #



# class ImagesFile(models.Model):
#     # image_outtake = models.ForeignKey(ProductionRawZimages)
#     # image_select = models.ForeignKey(PostReadyOriginal)
#     # image_select_thumb = models.ForeignKey(Zimages1Photoselects)
#     # image_select_push = models.ForeignKey(PushPhotoselects)
#     id = models.BigIntegerField(primary_key=True)
#     images = models.ManyToManyField(Images)
#     file_path  = models.ForeignKey(File)

#     class Meta:
#         db_table = 'images_file'
#         #unique_together = ('brand', 'vendor_style',)
#         #ordering = ['-colorstyle']

#     def __unicode__(self):
#         return self.file_path


# class PhotoAlbum(models.Model):
#     id = models.IntegerField(primary_key=True)
#     title = models.CharField(max_length=60)
#     public = models.IntegerField()

#     class Meta:
#         db_table = 'photo_album'


# class PhotoEvent(models.Model):
#     photo_event_id = models.IntegerField(primary_key=True)
#     event_id = models.CharField(max_length=50)
#     event_title = models.CharField(max_length=50)

#     class Meta:
#         db_table = 'photo_event'
#         ordering = ['-event_id']

#     def __unicode__(self):
#         return self.event_id


# class PhotoImages(models.Model):
#     id = models.IntegerField(primary_key=True)
#     title = models.CharField(max_length=60, blank=True)
#     images = models.ManyToManyField(Images)
#     created = models.DateTimeField()
#     rating = models.IntegerField()
#     width = models.IntegerField(null=True, blank=True)
#     height = models.IntegerField(null=True, blank=True)
#     user = models.ForeignKey(AuthUser, null=True, blank=True)

#     class Meta:
#         db_table = 'photo_images'


# class ImagesAlbum(models.Model):
#     id = models.IntegerField(primary_key=True)
#     images = models.ManyToManyField(Images)
#     albums = models.ManyToManyField(Album)

#     class Meta:
#         db_table = 'images_album'


# class ImagesTag(models.Model):
#     id = models.IntegerField(primary_key=True)
#     images = models.ManyToManyField(Images)
#     tags = models.ManyToManyField(Tag)

#     class Meta:
#         db_table = 'images_tags'


# class ImagesMetadata(models.Model):
#     id = models.IntegerField(primary_key=True)
#     images = models.ManyToManyField(Images)
#     metadatas = models.ManyToManyField(Metadata)
#     class Meta:
#         db_table = 'images_metadata'



# ###### Admin Classes and Config ########
# from django.contrib import admin
# #admin.autodiscover()


# class ProductAdmin(admin.ModelAdmin):
#     search_fields = ["colorstyle"] #, "brand", "category"]
# #    list_display = ["__unicode__", "photo_date", "brand", "po_number", "gender", "category", "product_type", "product_subtype", "sample_image_dt", "sample_location", "user"]
#     list_display = ["__unicode__", "colorstyle", "photo_date", "brand", "category"]
#     #"tags_", "albums_",        "thumbnail", "created"]
#     list_filter = ["alt", "brand", "colorstyle", "color", "category", "po_type"]
#     #list_filter = ["tags", "albums", "user"]

#     def save_model(self, request, obj, form, change):
#         obj.user = request.user
#         obj.save()
#         obj.user = request.user
#         obj.save()

# # class ImagesAdmin(admin.ModelAdmin):
# #     # search_fields = ["title"]
# #     list_display = ["__unicode__", "title", "user", "rating", "size", "tags_", "albums_",
# #         "thumbnail", "created"]
# #     list_filter = ["tags", "albums", "user"]

# #     def save_model(self, request, obj, form, change):
# #         obj.user = request.user
# #         obj.save()
# #         obj.user = request.user
# #         obj.save()


# class ImagesAdmin(admin.ModelAdmin):
#     search_fields = ["colorstyle", "photo_date"]
#     list_display = ["__unicode__", "colorstyle", "alt", "photo_date", "shot_number"]
#     #, "size", "tags_", "albums_",
#     #    "thumbnail", "created"]
#     list_filter = ["colorstyle", "photo_date"]

#     def save_model(self, request, obj, form, change):
#         obj.user = request.user
#         obj.save()
#         obj.user = request.user
#         obj.save()


# # admin.site.register(Album, AlbumAdmin)
# # admin.site.register(Tag, TagAdmin)
# # admin.site.register(Images, ImagesAdmin)
# admin.site.register(Product, ProductAdmin)

# ############# End Admin Configs ###########
