# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import ProfileForm, pre_fill_profile, MailForm, AddressForm, pre_fill_address, PhoneForm, pre_fill_phone
from location.models import Location, RideMatches
from location.script import find_coordinates
from users.models import Favorites, Address, PhoneNumber, Photo


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
    try:
        dest = User.objects.get(pk=user_id)
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
    except User.DoesNotExist:
        request.user.message_set.create(message='L\'utilisateur demandé n\'existe pas')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
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

@login_required
def add_phone(request):
    if request.method == 'POST':
        form = PhoneForm(request.POST)
        if form.is_valid():
            phone = PhoneNumber(number=form.cleaned_data['phone'],user=request.user)
            phone.save()
            request.user.message_set.create(message="Numéro de téléphone ajouté.")
            return HttpResponseRedirect('/users/phone/edit/%s'%phone.id)
        else:
            return render_to_response('users/add_phone.html', {'form':form},RequestContext(request))
    else:
        form = PhoneForm()
        return render_to_response('users/add_phone.html', {'form':form},RequestContext(request))
@login_required
def edit_phone(request, phone_id):
    try:
        phone = PhoneNumber.objects.get(pk=phone_id)
        if request.method == 'POST':
            form = PhoneForm(request.POST)
            if form.is_valid():
                phone.number = form.cleaned_data['phone']
                phone.save()
                request.user.message_set.create(message="Numéro de téléphone modifié.")
                return HttpResponseRedirect('/users/phone/edit/%d'% phone.id)
            else:
                return render_to_response('users/add_phone.html', {'form':form},RequestContext(request))
        else:
            data = pre_fill_phone(phone)
            form = PhoneForm(data)
            return render_to_response('users/add_phone.html', {'form':form},RequestContext(request))
    except PhoneNumber.DoesNotExist:
        request.user.message_set.create(message="Le numéro de téléphone demandé n'existe pas.")
        return HttpResponseRedirect('/users/profile/')
@login_required
def delete_phone(request, phone_id):
    try:
        PhoneNumber.objects.get(pk=phone_id).delete()
        request.user.message_set.create(message="Numéro de téléphone supprimé.")
        return HttpResponseRedirect('/users/%d/'% request.user.id)
    except Address.DoesNotExist:
        request.user.message_set.create(message="L'adresse demandée n'existe pas.")
        return HttpResponseRedirect('/users/%d/'% request.user.id)
@login_required
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            location = Location(house_number=form.cleaned_data['house_number'],
                                street=form.cleaned_data['street'],
                                city_name=form.cleaned_data['city_name'],
                                zip_code=form.cleaned_data['zip_code'])
            location.save()
            coord = find_coordinates(location.house_number,location.street,location.zip_code,location.city_name)
            location.latitude = float(coord.split(",")[2])
            location.longitude = float(coord.split(",")[3])
            location.save()
            address = Address(user=request.user,location=location)
            address.save()
            request.user.message_set.create(message="Adresse ajoutée.")
            return HttpResponseRedirect('/users/address/edit/%s'%address.id)
        else:
            return render_to_response('users/add_address.html', {'form':form},RequestContext(request))
    else:
        form = AddressForm()
        return render_to_response('users/add_address.html', {'form':form},RequestContext(request))
@login_required
def edit_address(request, address_id):
    try:
        address = Address.objects.get(pk=address_id)
        if request.method == 'POST':
            form = AddressForm(request.POST)
            if form.is_valid():
                address.location.house_number = form.cleaned_data['house_number']
                address.location.street = form.cleaned_data['street']
                address.location.city_name = form.cleaned_data['city_name']
                address.location.zip_code = form.cleaned_data['zip_code']
                address.location.save()
                coord = find_coordinates(address.location.house_number,address.location.street,address.location.zip_code,address.location.city_name)
                address.location.latitude = float(coord.split(",")[2])
                address.location.longitude = float(coord.split(",")[3])
                address.location.save()
                print address.location.city_name
                request.user.message_set.create(message="Adresse modifiée.")
                return HttpResponseRedirect('/users/address/edit/%d'% address.id)
            else:
                return render_to_response('users/add_address.html', {'form':form},RequestContext(request))
        else:
            data = pre_fill_address(address)
            form = AddressForm(data)
            return render_to_response('users/add_address.html', {'form':form},RequestContext(request))
    except Address.DoesNotExist:
        request.user.message_set.create(message="L'adresse demandée n'existe pas.")
        return HttpResponseRedirect('/users/profile/')
@login_required
def delete_address(request, address_id):
    try:
        Address.objects.get(pk=address_id).delete()
        request.user.message_set.create(message="Adresse supprimée.")
        return HttpResponseRedirect('/users/%d/'% request.user.id)
    except Address.DoesNotExist:
        request.user.message_set.create(message="L'adresse demandée n'existe pas.")
        return HttpResponseRedirect('/users/%d/'% request.user.id)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            return HttpResponseRedirect('/users/%d/'%request.user.id)
        else:
            return render_to_response('users/details.html', {'form':form}, RequestContext(request))
    else:
        data = pre_fill_profile(request.user)
        form = ProfileForm(data)
        return render_to_response('users/details.html', {'form':form}, RequestContext(request))

@login_required
def user_profile(request,user_id):
    ref = request.META.get('HTTP_REFERER')
    try:
        visited_user = User.objects.get(pk=user_id)
        fav = visited_user in request.user.favorites_owner.all()
        data = pre_fill_profile(request.user)
        form = ProfileForm(data)
        return render_to_response('users/details.html',{'visited_user':visited_user,'fav':fav,'ref':ref,'form':form},RequestContext(request))
    except User.DoesNotExist:
        request.user.message_set.create(message="L'utilisateur demandé n'existe pas.")
        return HttpResponseRedirect(ref)