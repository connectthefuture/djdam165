#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################

import django.forms as forms
from django.forms import Form
from django.forms import ModelChoiceField
from django.forms import ChoiceField
from accounts.models import *

# forms.py
import floppyforms as forms


class DatePicker(forms.DateInput):
    template_name = 'datepicker.html'

    class Media:
        js = (
            'js/jquery.min.js',
            'js/jquery-ui.min.js',
        )
        css = {
            'all': (
                'css/jquery-ui.css',
            )
        }


class DateForm(forms.Form):
    date = forms.DateField(widget=DatePicker)
