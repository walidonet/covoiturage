from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    (r'^ride/edit/(?P<ride_id>\d)+/$', edit_ride),
    (r'^ride/delete/(?P<ride_id>\d)+/$', delete_ride),
    (r'^ride/add/$', add_ride),
    (r'^passenger/edit/(?P<passenger_id>\d)+/$', edit_passenger),
    (r'^passenger/delete/(?P<passenger_id>\d)+/$', delete_passenger),
    (r'^passenger/search/(?P<passenger_id>\d)+/$', search),
    (r'^passenger/add/$', add_passenger),
	(r'^ride/$', list_ride),
)