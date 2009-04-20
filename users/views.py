# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from forms import UserForm, pre_fill
from location.models import Location
from location.script import find_coordinates
from users.models import Favorites, UserProfile


@login_required
def send_email(request, user_id):
    dest = get_object_or_404(User,pk=user_id)
    if request.method == 'POST':
        subject = request.POST.get('subject', '')
        message= ''+request.user.username + ' vous a envoye ce message. Pour lui repondre, rendez vous sur http://127.0.0.1:8000/users/%d/ .\n\n\n\n' % (request.user.id)
        message += request.POST.get('message', '')
        if subject and message:
            try:
                send_mail(subject,message,'nawak@test.com',[dest.email])
            except  BadHeaderError:
                request.user.message_set.create(message='Veuillez compléter les champs demandés correctement')
                return HttpResponseRedirect('/users/'+user_id+'/mail')
            request.user.message_set.create(message='Message envoyé')
            return HttpResponseRedirect('/users/'+user_id)
    else:
        return render_to_response('users/mail.html', {'dest':dest}, RequestContext(request))

@login_required
def users_list(request):
    users_list = User.objects.all().order_by('username')
    user_fav_list = request.user.favorites_owner.all()
    favorites = [fav.favorite for fav in user_fav_list]
    return render_to_response('users/user_list.html', {'users_list': users_list,'favorites':favorites}, RequestContext(request))
    
@login_required    
def add_favorite(request,user_id):
    ref = request.META.get('HTTP_REFERER')
    u = User.objects.get(pk=user_id)
    exists = Favorites.objects.filter(user=request.user,favorite=u)
    if exists.count() == 0:
        fav = Favorites(user=request.user,favorite=u)
        fav.save()
    return HttpResponseRedirect(ref)

@login_required
def delete_favorite(request,user_id):
    ref = request.META.get('HTTP_REFERER')
    u = User.objects.get(pk=user_id)
    Favorites.objects.get(user=request.user,favorite=u).delete()
    return HttpResponseRedirect(ref)


def extract(form, profile):
    if form.is_valid():
        req = find_coordinates(form.cleaned_data['house_number'],form.cleaned_data['street'],form.cleaned_data['zip_code'],form.cleaned_data['city_name'])
        try:
            if not profile.location == None:
                profile.location.street = form.cleaned_data['street']
                profile.location.house_number = form.cleaned_data['house_number']
                profile.location.city_name = form.cleaned_data['city_name']
                profile.location.zip_code = form.cleaned_data['zip_code']
                profile.location.latitude = float(req.split(",")[2])
                profile.location.longitude = float(req.split(",")[3])
                profile.location.save()
        except Location.DoesNotExist:        
            location = Location(street=form.cleaned_data['street'],
                                house_number=form.cleaned_data['house_number'],
                                city_name = form.cleaned_data['city_name'],
                                zip_code= form.cleaned_data['zip_code'],
                                latitude = float(req.split(",")[2]),
                                longitude= float(req.split(",")[3]))
            location.save()
            profile.location = location
        profile.phone_number = form.cleaned_data['phone_number']
        profile.mobile_phone_number = form.cleaned_data['mobile_phone_number']
        profile.save()
        return 'Vos données ont bien été modifiées'
    else:
        return 'Une erreur s\'est produite'

@login_required
def own_profile(request):
    try:
        profile = request.user.get_profile()
        if request.method == 'POST':
            form = UserForm(request.POST)
            profile.user = request.user
            request.user.message_set.create(message=extract(form,profile))
            return render_to_response('users/fill_profile.html',{'form':form,'profile':profile}, RequestContext(request))
        else:
            data = pre_fill(profile)
            form = UserForm(data)
            return render_to_response('users/fill_profile.html',{'form':form,'profile':profile})
    except UserProfile.DoesNotExist:
        if request.method == 'POST':
            form = UserForm(request.POST)
            profile = UserProfile(user=request.user)
            request.user.message_set.create(message=extract(form,profile))
            return render_to_response('users/fill_profile.html',{'form':form,'profile':profile}, RequestContext(request))
        else:
            form = UserForm()
            request.user.message_set.create(message="Veuillez compléter vos informations personnelles")
            return render_to_response('users/fill_profile.html',{'form':form}, RequestContext(request))

@login_required
def user_profile(request,user_id):
    visited_user = get_object_or_404(User,pk=user_id)
    ref = request.META.get('HTTP_REFERER')
    try:
        visited_user_profile = visited_user.get_profile()
        user_fav_list = request.user.favorites_owner.all()
        favorites = [fav.favorite for fav in user_fav_list]
        return render_to_response('users/details.html',{'visited_user':visited_user, 'visited_user_profile':visited_user_profile,'favorites':favorites,'referer':ref},RequestContext(request))
    except UserProfile.DoesNotExist:
        request.user.message_set.create(message="L'utilisateur "+visited_user.username+" n\'a pas encore rempli son profil")
        return render_to_response('users/details.html',{'referer':ref}, RequestContext(request))
            