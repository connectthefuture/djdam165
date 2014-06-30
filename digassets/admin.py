#!/usr/bin/env python
# -*- coding: utf-8 -*-
## admin.py
# adminactions  ####
from django.contrib.admin import site
import adminactions.actions as actions


# register all adminactions
actions.add_to_site(site)


###### Admin Classes and Config ########
# from django.db import models
# models.get_apps()

### This is the key to fixing Admin ViewDoesNotExist
#from django.contrib.sites.models import Site

from digassets.models import *
from django.contrib import admin
admin.autodiscover()

############# End Admin Configs ###########
