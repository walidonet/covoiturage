from django.conf.urls.defaults import *
import os
import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
     (r'^admin/(.*)', admin.site.root),
     (r'^accounts/', include('registration.urls')),
     (r'^users/', include('users.urls')),
     (r'^location/', include('location.urls')),
     (r'^news/', include('news.urls')),
     (r'^$', 'news.views.news_view'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': os.path.join(os.path.dirname(__file__), 'media')}),
 )