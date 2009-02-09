# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from users.models import Favorites, UserProfile
from location.models import Location
from django.template import RequestContext
from django.http import HttpResponseRedirect
from forms import UserForm
import urllib

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
#TODO ajouter une redirection vers la page d'ou on vient -> Trouver cette page (http referer)

@login_required
def delete_favorite(request,user_id):
    ref = request.META.get('HTTP_REFERER')
    u = User.objects.get(pk=user_id)
    Favorites.objects.get(user=request.user,favorite=u).delete()
    return HttpResponseRedirect(ref)

def extract(form, profile):
    if form.is_valid():
        query = '%d+%s,+%d,+%s,+Belgium' % (form.cleaned_data['house_number'],form.cleaned_data['street'].replace(' ','+'),form.cleaned_data['zip_code'],form.cleaned_data['city_name'].replace(' ','+'))
        url = 'http://maps.google.com/maps/geo?q=%s&output=csv&oe=utf8&sensor=true_or_false&key=your_api_key' % (query)
        req = urllib.urlopen(url).read()
        print url
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
def user_profile(request):
    try:
        profile = request.user.get_profile()
        if request.method == 'POST':
            form = UserForm(request.POST)
            profile.user = request.user
            message = extract(form,profile)
            return render_to_response('users/fill_profile.html',{'form':form,'profile':profile,'message':message})
        else:
            form = UserForm()
            return render_to_response('users/fill_profile.html',{'form':form,'profile':profile})
    except UserProfile.DoesNotExist:
        if request.method == 'POST':
            form = UserForm(request.POST)
            profile = UserProfile(user=request.user)
            message = extract(form,profile)
            return render_to_response('users/fill_profile.html',{'form':form,'profile':profile,'message':message})
        else:
            form = UserForm()
            return render_to_response('users/fill_profile.html',{'form':form})