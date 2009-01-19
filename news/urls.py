from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
	(r'^$', news_view),
)