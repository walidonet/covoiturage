from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    (r'^edit/(?P<news_id>\d)+/$', edit),
    (r'^delete/(?P<news_id>\d)+/$', delete),
    (r'^add$', add),
	(r'^$', news_view),
)