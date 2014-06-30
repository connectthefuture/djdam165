#!/usr/bin/env python
# -*- coding: utf-8 -*-
## admin.py
# adminactions  ####
from django.contrib.admin import site
import adminactions.actions as actions
from accounts.models import *
from django.contrib import admin
admin.autodiscover()

############# End Admin Configs ###########
