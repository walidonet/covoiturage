from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    (r'^ride/edit/(?P<ride_id>\d)+/$', edit_ride),
    (r'^ride/delete/(?P<ride_id>\d)+/$', delete_ride),
    (r'^ride/add/$', add_ride),
	(r'^ride/$', list_ride),
)