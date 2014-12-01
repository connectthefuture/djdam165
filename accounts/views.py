# -*- coding: utf-8 -*-
# Create your views here.

####################
####################################################
####################################################
#### Django --> REST Framework
#######################################################
# ###################
####################################################
####################
###
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from accounts.serializers import UserSerializer, GroupSerializer
from accounts.permissions import IsStaffOrTargetUser


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

####################################################
############
####################################################
####################################################
############
####################################################

from searcher.models import PostReadyOriginal, ProductSnapshotLive, ExcelToolData
from accounts.serializers import PostReadyOriginalSerializer, ProductSnapshotLiveSerializer, ExcelToolDataSerializer

class PostReadyOriginalViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows PostReadyOriginal to be viewed or edited.
    """
    queryset = PostReadyOriginal.objects.all()
    serializer_class = PostReadyOriginalSerializer

class ProductSnapshotLiveViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ProductSnapshotLive to be viewed or edited.
    """
    queryset = ProductSnapshotLive.objects.all()
    serializer_class = ProductSnapshotLiveSerializer

class ExcelToolDataViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ExcelToolData to be viewed or edited.
    """
    queryset = ExcelToolData.objects.all()
    serializer_class = ExcelToolDataSerializer


#####
#####

from searcher.models import SupplierIngest, SupplierIngest404, ImageUpdate, LookletShotList
from accounts.serializers import SupplierIngestSerializer, SupplierIngest404Serializer, ImageUpdateSerializer, LookletShotListSerializer

class SupplierIngestViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows SupplierIngest to be viewed or edited.
    """
    queryset = SupplierIngest.objects.all()
    serializer_class = SupplierIngestSerializer

class SupplierIngest404ViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows SupplierIngest404 to be viewed or edited.
    """
    queryset = SupplierIngest404.objects.all()
    serializer_class = SupplierIngest404Serializer

class ImageUpdateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ImageUpdate to be viewed or edited.
    """
    queryset = ImageUpdate.objects.all()
    serializer_class = ImageUpdateSerializer


class LookletShotListViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows LookletShotList to be viewed or edited.
    """
    queryset = LookletShotList.objects.all()
    serializer_class = LookletShotListSerializer


## REST_FRAMEWORK Browsable views
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['GET', 'POST', 'PUT'])
@permission_classes((IsAuthenticated, ))
def image_update_list(request, pk=None, alt=1, colorstyle=None):
    """
    List all image_updates, or create a new image_update.
    """
    if request.method == 'GET':
        image_updates = ImageUpdate.objects.all()
        serializer = ImageUpdateSerializer(image_updates, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ImageUpdateSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    elif request.method == 'PUT':
        if not colorstyle:
            colorstyle = request.DATA['colorstyle']
        try:
            image_update = ImageUpdate.objects.get(colorstyle=colorstyle,alt=alt)
        except ImageUpdate.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ImageUpdateSerializer(image_update, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'POST'])
@permission_classes((IsAuthenticated,))
def image_update_detail(request, format=None, pk=None,alt=1,colorstyle=None):
    """
    Retrieve, update or delete an ImageUpdate instance.
    """
    try:
        if not colorstyle:
            colorstyle = request.GET['colorstyle']
    except:
        pass
    try:
        image_update = ImageUpdate.objects.get(colorstyle=colorstyle, alt=1)
    except ImageUpdate.DoesNotExist:
        try:
            image_update = ImageUpdate.objects.get(colorstyle=colorstyle,alt=alt)
        except ImageUpdate.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ImageUpdateSerializer(image_update)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if not colorstyle:
            colorstyle = request.DATA['colorstyle']
        image_update = ImageUpdate.objects.get(colorstyle=colorstyle, alt=alt)
        serializer = ImageUpdateSerializer(image_update, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST':
        serializer = ImageUpdateSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        image_update = ImageUpdate.objects.get(colorstyle=colorstyle, alt=alt)
        image_update.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


## angular and rest
from django.views.generic.base import TemplateView

####### Angular API #######

class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    model = User

    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (AllowAny() if self.request.method == 'POST'
                else IsStaffOrTargetUser()),

###################################
###################################

from django.contrib.auth import login, logout
from . import authentication

class AuthView(TemplateView):
    authentication_classes = (authentication.QuietBasicAuthentication,)

    def post(self, request, *args, **kwargs):
        login(request, request.user)
        return Response(UserSerializer(request.user).data)

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response({})


####################

class OnePageAppView(TemplateView):
    template_name = 'one_page_app.html'


####################
####################
####################
@api_view(['GET', 'POST', 'PUT'])
@permission_classes((IsAuthenticated, ))
def looklet_shot_list_update_list(request,
                                  content_format=None,
                                  pk=None,
                                  colorstyle=None,
                                  photodate=None,
                                  reshoot=False,
                                  timestamp=None,
                                  username=None):
    """
    List all looklet_shot_list_updates, or create a new looklet_shot_list_update.
    """

    if request.method == 'GET':
        looklet_shot_list_updates = LookletShotList.objects.all()
        serializer = LookletShotListSerializer(looklet_shot_list_updates, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = LookletShotListSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        if not colorstyle:
            colorstyle = request.DATA['colorstyle']
        try:
            looklet_shot_list_update = LookletShotList.objects.get(colorstyle=colorstyle)
        except LookletShotList.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LookletShotListSerializer(looklet_shot_list_update,
                                               data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'POST'])
@permission_classes((IsAuthenticated,))
def looklet_shot_list_update_detail(request,
                                    content_format=None,
                                    pk=None,
                                    colorstyle=None,
                                    photodate=None,
                                    reshoot=False,
                                    timestamp=None,
                                    username=None):
    """
    Retrieve, update or delete an LookletShotList instance.
    """
    if not colorstyle:
        colorstyle = request.DATA['colorstyle']
        #photodate = request.DATA['photodate']
        pass

    looklet_shot_list_update = ''
    try:
        looklet_shot_list_update = LookletShotList.objects.get(colorstyle=colorstyle)
    except LookletShotList.DoesNotExist:
        pass
        # try:
        #     looklet_shot_list_update = LookletShotList.objects.get(colorstyle=colorstyle)
        # except LookletShotList.DoesNotExist:
        #     return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        if not looklet_shot_list_update:
            looklet_shot_list_updates = LookletShotList.objects.all()
        else:
            looklet_shot_list_updates = looklet_shot_list_update
        serializer = LookletShotListSerializer(looklet_shot_list_updates, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = LookletShotListSerializer(data=request.DATA)
        try:
            looklet_shot_list_update = LookletShotList.objects.get(colorstyle=colorstyle)
            pass
        except LookletShotList.DoesNotExist:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        if not colorstyle:
            colorstyle = request.DATA['colorstyle']
        looklet_shot_list_update = LookletShotList.objects.get(colorstyle=colorstyle
                                                               )
        serializer = LookletShotListSerializer(looklet_shot_list_update,
                                               data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        looklet_shot_list_update = LookletShotList.objects.get(colorstyle=colorstyle)
        looklet_shot_list_update.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

