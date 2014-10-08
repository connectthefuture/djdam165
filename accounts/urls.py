##### REST Auth persistent login
from django.conf.urls import patterns, include, url

from . import views

# Additionally, we include login URLs for the browseable API.
from rest_framework.urlpatterns import format_suffix_patterns


#### REST FRAMWORK URLS Views in Accounts for now
urlpatterns = patterns('accounts.views',
    url(r'^image-update-list/$', 'image_update_list'),
    url(r'^image-update/(?P<colorstyle>[0-9]{9}).*?/$', 'image_update_detail'),
    url(r'^image-update-detail/$', 'image_update_detail'),
    url(r'^image-update/?$', 'image_update_list'),
)
urlpatterns = format_suffix_patterns(urlpatterns)


urlpatterns += patterns('',
    (r'^login$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}),
    (r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    (r'^password_change$', 'django.contrib.auth.views.password_change', {'template_name': 'accounts/password_change_form.html'}),
    (r'^password_change_done$', 'django.contrib.auth.views.password_change_done', {'template_name': 'accounts/password_change_done.html'}),
    url(r'^api/auth/$', api_views.AuthView.as_view(), name='authenticate'),
)


# Angularjs 1 page app
urlpatterns += patterns('accounts.views',
                        url(r'^$', OnePageAppView.as_view(), name='onepagehome'),
                        )
