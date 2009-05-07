from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    (r'^address/add/$', add_address),
    (r'^address/edit/(?P<address_id>\d)+/$', edit_address),
    (r'^address/delete/(?P<address_id>\d)+/$', delete_address),
    (r'^phone/add/$', add_phone),
    (r'^phone/edit/(?P<phone_id>\d)+/$', edit_phone),
    (r'^phone/delete/(?P<phone_id>\d)+/$', delete_phone),
    (r'^photo/add/$', add_photo),
    (r'^add_favorite/(?P<user_id>\d)+/$', add_favorite),
    (r'^delete_favorite/(?P<user_id>\d)+/$', delete_favorite),
    (r'^edit/$', edit_profile),
    (r'^(?P<user_id>\d)+/mail_c/(?P<match_id>\d)+/$', send_email_covoiturage),
    (r'^(?P<user_id>\d)+/mail/$', send_email),
    (r'^(?P<user_id>\d)+/$', user_profile),
    (r'^change_password/$', password_change, {'post_change_redirect': '/users/change_password/'}),
    (r'^mail_me/$', email_me),
    (r'^signup/$', check_signup_password),
    (r'^$', users_list),
)