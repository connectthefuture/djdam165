#!/usr/bin/env python
# -*- coding: utf-8 -*-

## forms.py
# from django.forms import forms

# class SelectWidgetBootstrap(forms.Select):
#     """
#     http://twitter.github.com/bootstrap/components.html#buttonDropdowns
#     Needs bootstrap and jquery
#     """
#     js = ("""
#     <script type="text/javascript">
#         function setBtnGroupVal(elem) {
#             btngroup = $(elem).parents('.btn-group');
#             selected_a = btngroup.find('a[selected]');
#             if (selected_a.length > 0) {
#                 val = selected_a.attr('data-value');
#                 label = selected_a.html();
#             } else {
#                 btngroup.find('a').first().attr('selected', 'selected');
#                 setBtnGroupVal(elem);
#             }
#             btngroup.find('input').val(val);
#             btngroup.find('.btn-group-label').html(label);
#         }
#         $(document).ready(function() {
#             $('.btn-group-form input').each(function() {
#                 setBtnGroupVal(this);
#             });
#             $('.btn-group-form li a').click(function() {
#                 $(this).parent().siblings().find('a').attr('selected', false);
#                 $(this).attr('selected', true);
#                 setBtnGroupVal(this);
#             });
#         })
#     </script>
#     """)
#     def __init__(self, attrs={'class': 'btn-group pull-left btn-group-form'}, choices=()):
#         self.noscript_widget = forms.Select(attrs={}, choices=choices)
#         super(SelectWidgetBootstrap, self).__init__(attrs, choices)
    
#     def __setattr__(self, k, value):
#         super(SelectWidgetBootstrap, self).__setattr__(k, value)
#         if k != 'attrs':
#             self.noscript_widget.__setattr__(k, value)
    
#     def render(self, name, value, attrs=None, choices=()):
#         if value is None: value = ''
#         final_attrs = self.build_attrs(attrs, name=name)
#         output = ["""<div%(attrs)s>"""
#                   """    <button class="btn btn-group-label" type="button">%(label)s</button>"""
#                   """    <button class="btn dropdown-toggle" type="button" data-toggle="dropdown">"""
#                   """        <span class="caret"></span>"""
#                   """    </button>"""
#                   """    <ul class="dropdown-menu">"""
#                   """        %(options)s"""
#                   """    </ul>"""
#                   """    <input type="hidden" name="%(name)s" value="" class="btn-group-value" />"""
#                   """</div>"""
#                   """%(js)s"""
#                   """<noscript>%(noscript)s</noscript>"""
#                    % {'attrs': flatatt(final_attrs),
#                       'options':self.render_options(choices, [value]),
#                       'label': _(u'Select an option'),
#                       'name': name,
#                       'js': SelectWidgetBootstrap.js,
#                       'noscript': self.noscript_widget.render(name, value, {}, choices)} ]
#         return mark_safe(u'\n'.join(output))

#     def render_option(self, selected_choices, option_value, option_label):
#         option_value = force_unicode(option_value)
#         selected_html = (option_value in selected_choices) and u' selected="selected"' or ''
#         return u'<li><a href="javascript:void(0)" data-value="%s"%s>%s</a></li>' % (
#             escape(option_value), selected_html,
#             conditional_escape(force_unicode(option_label)))

#     def render_options(self, choices, selected_choices):
#         # Normalize to strings.
#         selected_choices = set([force_unicode(v) for v in selected_choices])
#         output = []
#         for option_value, option_label in chain(self.choices, choices):
#             if isinstance(option_label, (list, tuple)):
#                 output.append(u'<li class="divider" label="%s"></li>' % escape(force_unicode(option_value)))
#                 for option in option_label:
#                     output.append(self.render_option(selected_choices, *option))
#             else:
#                 output.append(self.render_option(selected_choices, option_value, option_label))
#         return u'\n'.join(output)


# class TestForm(forms.Form):
#     group = forms.ModelChoiceField(models.Group.objects.all(), widget=SelectWidgetBootstrap(),
#                                    empty_label=_(u'(no group selected)'))

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


## handle add and update events
#if request.method == 'POST':
#    if request.POST['submit_action'] == 'search_styles':
#  # attempt to do update
#        colorstyles_list = []
#        for k, v in request.POST.iteritems():
#
#            found_obj = Production_Raw_Outtakes.objects.get(
#                pk=request.POST['colorstyle'])
#            colorstyles_list.append(found_obj)
#
## get existing contacts
#response = SearchForm.objects.all()
#response = colorstyle_query_results(colorstyles_list)
#return render_to_response('search_results.html', 'results': response,)



# from __future__ import absolute_import
# import os.path
# import re

# from email.MIMEBase import MIMEBase

# from django.conf import settings
# from django.core.mail import EmailMultiAlternatives, SafeMIMEMultipart

# class EmailMultiRelated(EmailMultiAlternatives):
#     """
#     A version of EmailMessage that makes it easy to send multipart/related
#     messages. For example, including text and HTML versions with inline images.
    
#     @see https://djangosnippets.org/snippets/2215/
#     """
#     related_subtype = 'related'
    
#     def __init__(self, *args, **kwargs):
#         # self.related_ids = []
#         self.related_attachments = []
#         return super(EmailMultiRelated, self).__init__(*args, **kwargs)
    
#     def attach_related(self, filename=None, content=None, mimetype=None):
#         """
#         Attaches a file with the given filename and content. The filename can
#         be omitted and the mimetype is guessed, if not provided.

#         If the first parameter is a MIMEBase subclass it is inserted directly
#         into the resulting message attachments.
#         """
#         if isinstance(filename, MIMEBase):
#             assert content == mimetype == None
#             self.related_attachments.append(filename)
#         else:
#             assert content is not None
#             self.related_attachments.append((filename, content, mimetype))
    
#     def attach_related_file(self, path, mimetype=None):
#         """Attaches a file from the filesystem."""
#         filename = os.path.basename(path)
#         content = open(path, 'rb').read()
#         self.attach_related(filename, content, mimetype)
    
#     def _create_message(self, msg):
#         return self._create_attachments(self._create_related_attachments(self._create_alternatives(msg)))
    
#     def _create_alternatives(self, msg):       
#         for i, (content, mimetype) in enumerate(self.alternatives):
#             if mimetype == 'text/html':
#                 for related_attachment in self.related_attachments:
#                     if isinstance(related_attachment, MIMEBase):
#                         content_id = related_attachment.get('Content-ID')
#                         content = re.sub(r'(?<!cid:)%s' % re.escape(content_id), 'cid:%s' % content_id, content)
#                     else:
#                         filename, _, _ = related_attachment
#                         content = re.sub(r'(?<!cid:)%s' % re.escape(filename), 'cid:%s' % filename, content)
#                 self.alternatives[i] = (content, mimetype)
        
#         return super(EmailMultiRelated, self)._create_alternatives(msg)
    
#     def _create_related_attachments(self, msg):
#         encoding = self.encoding or settings.DEFAULT_CHARSET
#         if self.related_attachments:
#             body_msg = msg
#             msg = SafeMIMEMultipart(_subtype=self.related_subtype, encoding=encoding)
#             if self.body:
#                 msg.attach(body_msg)
#             for related_attachment in self.related_attachments:
#                 if isinstance(related_attachment, MIMEBase):
#                     msg.attach(related_attachment)
#                 else:
#                     msg.attach(self._create_related_attachment(*related_attachment))
#         return msg
    
#     def _create_related_attachment(self, filename, content, mimetype=None):
#         """
#         Convert the filename, content, mimetype triple into a MIME attachment
#         object. Adjust headers to use Content-ID where applicable.
#         Taken from http://code.djangoproject.com/ticket/4771
#         """
#         attachment = super(EmailMultiRelated, self)._create_attachment(filename, content, mimetype)
#         if filename:
#             mimetype = attachment['Content-Type']
#             del(attachment['Content-Type'])
#             del(attachment['Content-Disposition'])
#             attachment.add_header('Content-Disposition', 'inline', filename=filename)
#             attachment.add_header('Content-Type', mimetype, name=filename)
#             attachment.add_header('Content-ID', '<%s>' % filename)
#         return attachment
