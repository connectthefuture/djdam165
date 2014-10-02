# !/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'johnb'

from django.contrib.auth.models import User, Group
from searcher.models import PostReadyOriginal, ProductSnapshotLive, ExcelToolData
from rest_framework import serializers

class PostReadyOriginalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostReadyOriginal
        fields = ('colorstyle', 'alt', 'file_path', 'photo_date', 'image_type')

class ProductSnapshotLiveSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductSnapshotLive
        fields = ('colorstyle', 'brand', 'vendor_style', 'po_number', 'po_type', 'product_type', 'product_subtype')


class ExcelToolDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExcelToolData
        fields = ('colorstyle', 'brand', 'vendor_style', 'po_number','short_name', 'material', 'country_origin')


import autocomplete_light
from searcher.models import SupplierIngest
#(serializers.ModelSerializer):
class SupplierIngestSerializer(serializers.HyperlinkedModelSerializer):
    vendor_name = serializers.ChoiceField(
        widget=autocomplete_light.ChoiceWidget('VendorNameAutocomplete')
    )
    class Meta:
        model = SupplierIngest
        fields = ('colorstyle', 'vendor_name','vendor_brand', 'vendor_style', 'alt', 'image_url', 'image_type', 'modified_dt')


from searcher.models import SupplierIngest404
class SupplierIngest404Serializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = SupplierIngest404
       fields = ('colorstyle','alt', 'error_code', 'image_url', 'modified_dt')


from searcher.models import ImageUpdate
class ImageUpdateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ImageUpdate
        fields = ('colorstyle', 'alt', 'create_dt', 'modify_dt')




class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')