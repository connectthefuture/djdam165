# !/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'johnb'

from django.contrib.auth.models import User, Group
from models import PostReadyOriginal, ProductSnapshotLive, ExcelToolData
from rest_framework import serializers

class PostReadyOriginalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostReadyOriginal
        fields = ('colorstyle', 'alt', 'file_path', 'photo_date')

class ProductSnapshotLiveSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductSnapshotLive
        fields = ('colorstyle', 'brand', 'vendor_style', 'po_number', 'po_type', 'product_type', 'product_subtype')


class ExcelToolDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExcelToolData
        fields = ('colorstyle', 'brand', 'vendor_style', 'po_number','short_name', 'material', 'country_origin')

from searcher.models import SupplierIngest
class SupplierIngestSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = SupplierIngest
       fields = ('colorstyle', 'vendor_name','vendor_brand', 'vendor_style', 'image_number', 'image_url', 'image_type', 'modified_dt')

from searcher.models import SupplierIngest404
class SupplierIngest404Serializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = SupplierIngest404
       fields = ('colorstyle','alt', 'error_code', 'image_url', 'modified_dt')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')