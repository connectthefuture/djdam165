__author__ = 'johnb'
# Almost same import as in django.contrib.admin

from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.contrib.admin.options import ModelAdmin, HORIZONTAL, VERTICAL
from django.contrib.admin.options import StackedInline, TabularInline

# NOTICE: that we are not importing site here!
# basically this is the only one import you'll need
# other imports required if you want easy replace standard admin package with yours
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.filters import (ListFilter, SimpleListFilter,
    FieldListFilter, BooleanFieldListFilter, RelatedFieldListFilter,
    ChoicesFieldListFilter, DateFieldListFilter, AllValuesFieldListFilter)

# Let's create AdminSite instance
# NOTICE: here you can ovverride admin class and create your own AdminSite implementation
# IF you do not want to change admin.py than you should
# monkey patch django.contrib.admin module
# in admin_custom.py
# Right after
site = AdminSite()

import django.contrib.admin
django.contrib.admin.site = site

# By the way now you can use the standard django admin autodiscover function
# you can import it here
from django.contrib.admin import autodiscover
# Add
# Monkey patch django admin_tools
import admin_tools.utils
admin_tools.utils.admin.site = site

#
# # add this code
# import django.contrib.admin
# django.contrib.admin.site = site
#
# # By the way now you can use the standard django admin autodiscover function
# # you can import it here
# from django.contrib.admin import autodiscover
# site = AdminSite()


def autodiscover():
    """
    Autodiscover function from django.contrib.admin
    """

    import copy
    from django.conf import settings
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)

        try:
            before_import_registry = copy.copy(site._registry)
            import_module('%s.admin' % app)
        except:
            site._registry = before_import_registry
            if module_has_submodule(mod, 'admin'):
                raise