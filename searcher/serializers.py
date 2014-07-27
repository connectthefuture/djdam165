# !/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'johnb'

from django.contrib.auth.models import User, Group
from models import PostReadyOriginal, ProductSnapshotLive
from rest_framework import serializers

class PostReadyOriginalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostReadyOriginal
        fields = ('colorstyle', 'alt', 'file_path', 'photo_date')

class ProductSnapshotLiveSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductSnapshotLive
        fields = ('colorstyle', 'brand', 'vendor_style', 'po_number')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')