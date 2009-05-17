from os.path import splitext
from settings import MEDIA_ROOT
import os
def handle_uploaded_file(f,user):
    t, e = splitext(f.name)
    string = os.path.join(MEDIA_ROOT, 'users_pics', '%s%s' % (user.username, e))
    destination = open(string, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    return "%s%s" %(user.username,e)
