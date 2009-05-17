from os.path import splitext
def handle_uploaded_file(f,user):
    t, e = splitext(f.name)
    destination = open('./media/user_pics/%s%s'% (user.username,e), 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
