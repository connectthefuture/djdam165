#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'johnb'
from django import forms
import djdam.settings

class MultiSelectWidget(forms.SelectMultiple):
    class Media:
        css = {
            'all': (
                djdam.settings.MEDIA_URL + 'css/ui.multiselect.css',
            )
        }
        js = (
            djdam.settings.MEDIA_URL + 'js/plugins/tmpl/jquery.tmpl.1.1.1.js',
            djdam.settings.MEDIA_URL + 'js/plugins/blockUI/jquery.blockUI.js',
            djdam.settings.MEDIA_URL + 'js/ui.multiselect.js',
        )

    def __init__(self, language=None, attrs=None):
        self.language = language or djdam.settings.LANGUAGE_CODE[:2]
        super(MultiSelectWidget, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None):
        rendered = super(MultiSelectWidget, self).render(name, value, attrs)
        return rendered + mark_safe(u'''<script type="text/javascript">
            $(document).ready(function afterReady() {
                var elem = $('#id_%(name)s');
                elem.multiselect();
            });
            </script>''' % {'name':name})

