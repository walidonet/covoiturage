from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
     (r'^admin/(.*)', admin.site.root),
     (r'^accounts/', include('registration.urls')),
     (r'^users/', include('users.urls')),
     (r'^location/', include('location.urls')),
     (r'^news/', include('news.urls')),
)
