def handle_uploaded_file(f,user):
    print f.name
    destination = open('./media/user_pics/%s_%s'% (user.username,f.name), 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
