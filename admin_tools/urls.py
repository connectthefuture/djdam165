from django.conf import settings
try:
    from django.conf.urls import patterns, url, include
except ImportError: # django < 1.4
    from django.conf.urls import patterns, url, include

urls = []
if 'admin_tools.menu' in settings.INSTALLED_APPS:
    urls.append(url(r'^menu/', include('admin_tools.menu.urls')))
if 'admin_tools.dashboard' in settings.INSTALLED_APPS:
    urls.append(url(r'^dashboard/', include('admin_tools.dashboard.urls')))

urlpatterns = patterns('', *urls)
