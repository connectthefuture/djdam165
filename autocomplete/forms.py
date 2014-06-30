#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.core.urlresolvers import reverse
from searcher.models import ProductSnapshotLive
from searcher.fields import ProductSnapshotLiveAutoCompleteField

class TestForm(forms.Form):
    theField = ProductSnapshotLiveAutoCompleteField(lookup_url = reverse('ajax_pmstyle_list'),
                                                            model=ProductSnapshotLive, 
                                                            required=True)