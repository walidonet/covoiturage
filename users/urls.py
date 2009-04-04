from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    (r'^add_favorite/(?P<user_id>\d)+/$', add_favorite),
    (r'^delete_favorite/(?P<user_id>\d)+/$', delete_favorite),
    (r'^profile/$', own_profile),
    (r'^(?P<user_id>\d)+/$', user_profile),
    (r'^$', users_list),
)