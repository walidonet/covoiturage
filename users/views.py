# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from forms import ProfileForm, pre_fill, MailForm
from location.models import Location, RideMatches
from location.script import find_coordinates
from users.models import Favorites, UserProfile


def email_me(request):
    if request.method == 'POST':
        mailForm = MailForm(request.POST)
        if mailForm.is_valid():
            send_mail(mailForm.cleaned_data['subject'],mailForm.cleaned_data['message'],mailForm.cleaned_data['email'],['vhj2002@gmail.com'])
            return HttpResponseRedirect('/news/')
        else:
            return render_to_response('mail_me.html',{'mailForm':mailForm}, RequestContext(request))
    else:
        return render_to_response('mail_me.html',{'mailForm':MailForm()}, RequestContext(request))


@login_required
def send_email_covoiturage(request,user_id,match_id):
    try:
        dest = User.objects.get(pk=user_id)
        match = RideMatches.objects.get(pk=match_id)
        if request.method == 'POST':
            subject = u'Demande de covoiturage émanant de %s' % match.passenger_ride.passenger.username
            message = u'Vous avez reçu ce mail car il semblerait que vous puissiez répondre à une demande de covoiturage\n\nRendez-vous sur http://127.0.0.1:8000/location/ride/matches/%d pour en savoir plus. \n Ci-dessous se trouve le message que vous a laissé la personne ayant initié cette recherche\n --------------------------\n' % (match.id)
            message += request.POST.get('message')
            send_mail(subject, message,'nawak',[dest.email])
            match.contacted=True
            match.save()
            return HttpResponseRedirect('/location/ride/matches/')
        else:
            return render_to_response('users/mail_cov.html', RequestContext(request))
    except User.DoesNotExist:
        request.user.message_set.create(message='Cet utilisateur n\'existe pas')
        return HttpResponseRedirect('/location/ride/matches')
    except  RideMatches.DoesNotExist:
        request.user.message_set.create(message='Le trajet demandé n\'existe pas')
        return HttpResponseRedirect('/location/ride/matches')
@login_required
def send_email(request, user_id):
    dest = get_object_or_404(User,pk=user_id)
    if request.method == 'POST':
        subject = request.POST.get('subject', '')
        message= ''+request.user.username + u' vous a envoyé ce message. Pour lui répondre, rendez vous sur http://127.0.0.1:8000/users/%d/ .\n\n\n\n' % (request.user.id)
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
        coord1 = find_coordinates(form.cleaned_data['loc1_house_number'],form.cleaned_data['loc1_street'],form.cleaned_data['loc1_zip_code'],form.cleaned_data['loc1_city_name'])
        try:
            if not profile.location == None:
                profile.location.street = form.cleaned_data['loc1_street']
                profile.location.house_number = form.cleaned_data['loc1_house_number']
                profile.location.city_name = form.cleaned_data['loc1_city_name']
                profile.location.zip_code = form.cleaned_data['loc1_zip_code']
                profile.location.latitude = float(coord1.split(",")[2])
                profile.location.longitude = float(coord1.split(",")[3])
                profile.location.save()
            else:
                raise Location.DoesNotExist()
        except Location.DoesNotExist:        
            location1 = Location(street=form.cleaned_data['loc1_street'],
                                house_number=form.cleaned_data['loc1_house_number'],
                                city_name = form.cleaned_data['loc1_city_name'],
                                zip_code= form.cleaned_data['loc1_zip_code'],
                                latitude = float(coord1.split(",")[2]),
                                longitude= float(coord1.split(",")[3]))
            location1.save()
            profile.location = location1
        print "before"
        if not form.cleaned_data['loc2_street'] == '':
            print "AFTER"
            coord2 = find_coordinates(form.cleaned_data['loc2_house_number'],form.cleaned_data['loc2_street'],form.cleaned_data['loc2_zip_code'],form.cleaned_data['loc2_city_name'])
            try:
                print "Location2 : %s" % profile.location2
                if not profile.location2 == None:
                    profile.location2.street = form.cleaned_data['loc2_street']
                    profile.location2.house_number = form.cleaned_data['loc2_house_number']
                    profile.location2.city_name = form.cleaned_data['loc2_city_name']
                    profile.location2.zip_code = form.cleaned_data['loc2_zip_code']
                    profile.location2.latitude = float(coord2.split(",")[2])
                    profile.location2.longitude = float(coord2.split(",")[3])
                    profile.location2.save()
                    print "Location2 : %s" % profile.location2
                else:
                    raise Location.DoesNotExist()
            except Location.DoesNotExist:  
                print "Except"      
                location2 = Location(street=form.cleaned_data['loc2_street'],
                                    house_number=form.cleaned_data['loc2_house_number'],
                                    city_name = form.cleaned_data['loc2_city_name'],
                                    zip_code= form.cleaned_data['loc2_zip_code'],
                                    latitude = float(coord2.split(",")[2]),
                                    longitude= float(coord2.split(",")[3]))
                location2.save()
                print "Location2 : %s" % location2
                profile.location2 = location2
                print "Profile.Location2 : %s" % profile.location2
            if not form.cleaned_data['loc3_street'] == '':
                coord3 = find_coordinates(form.cleaned_data['loc3_house_number'],form.cleaned_data['loc3_street'],form.cleaned_data['loc3_zip_code'],form.cleaned_data['loc3_city_name'])
                try:
                    if not profile.location3 == None:
                        profile.location3.street = form.cleaned_data['loc3_street']
                        profile.location3.house_number = form.cleaned_data['loc3_house_number']
                        profile.location3.city_name = form.cleaned_data['loc3_city_name']
                        profile.location3.zip_code = form.cleaned_data['loc3_zip_code']
                        profile.location3.latitude = float(coord3.split(",")[2])
                        profile.location3.longitude = float(coord3.split(",")[3])
                        profile.location3.save()
                    else:
                        raise Location.DoesNotExist()
                except Location.DoesNotExist:        
                    location3 = Location(street=form.cleaned_data['loc3_street'],
                                        house_number=form.cleaned_data['loc3_house_number'],
                                        city_name = form.cleaned_data['loc3_city_name'],
                                        zip_code= form.cleaned_data['loc3_zip_code'],
                                        latitude = float(coord3.split(",")[2]),
                                        longitude= float(coord3.split(",")[3]))
                    location3.save()
                    profile.location3 = location3
        
        profile.phone_number1 = form.cleaned_data['phone_number1']
        profile.phone_number2 = form.cleaned_data['phone_number2']
        profile.phone_number3 = form.cleaned_data['phone_number3']
        profile.save()
        return 'Vos données personnelles ont bien été modifiées'
    else:
        return 'Une erreur s\'est produite'

@login_required
def own_profile(request):
    try:
        profile = request.user.get_profile()
        ref = request.META.get('HTTP_REFERER')
        if request.method == 'POST':
            form = ProfileForm(request.POST)
            request.user.message_set.create(message=extract(form,profile))
            return HttpResponseRedirect(ref)
        else:
            data = pre_fill(profile)
            form = ProfileForm(data)
            return render_to_response('users/fill_profile.html',{'form':form,'profile':profile}, RequestContext(request))
    except UserProfile.DoesNotExist:
        if request.method == 'POST':
            form = ProfileForm(request.POST)
            profile = UserProfile(user=request.user)
            request.user.message_set.create(message=extract(form,profile))
            return render_to_response('users/fill_profile.html',{'form':form,'profile':profile}, RequestContext(request))
        else:
            form = ProfileForm()
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
            