# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.serializers import serialize
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.utils import simplejson
from django.shortcuts import render_to_response, get_object_or_404
from forms import *
from location.models import *
from location.script import *
from users.models import *
from datetime import datetime

@login_required
def list_passenger(request):
    passengers = Passenger.objects.filter(Q(dateTime__gte=datetime.today) | Q(everyDay=True),passenger=request.user).order_by('dateTime')
    return render_to_response('location/my_passengers.html',{'passengers':passengers}, RequestContext(request))  

@login_required
def list_old_passenger(request):
    passengers = Passenger.objects.filter(Q(dateTime__lt=datetime.today) & Q(everyDay=False),passenger=request.user).order_by('dateTime')
    return render_to_response('location/passenger_archives.html',{'passengers':passengers}, RequestContext(request))

@login_required
def list_ride(request):
    rides = Ride.objects.filter(Q(dateTime__gte=datetime.today) | Q(everyDay=True),driver=request.user,).order_by('dateTime')
    return render_to_response('location/my_rides.html',{'rides':rides}, RequestContext(request))
    
@login_required
def list_old_ride(request):
    rides = Ride.objects.filter(Q(dateTime__lt=datetime.today) & Q(everyDay=False),driver=request.user).order_by('dateTime')
    return render_to_response('location/ride_archives.html',{'rides':rides}, RequestContext(request))

@user_passes_test(lambda u: u.has_perm('location.arrivals'), login_url='/news/')
def list_arrivals(request):
    arrivals = Arrivals.objects.all()
    return render_to_response('location/arrivals.html',{'arrivals':arrivals}, RequestContext(request))

@login_required
def list_matches(request):
    rides = request.user.ride_set.filter(Q(dateTime__gte=datetime.today) | Q(everyDay=True))
    passenger_rides = request.user.passenger_set.filter(Q(dateTime__gte=datetime.today) | Q(everyDay=True))
    return render_to_response('location/matches.html',{'rides':rides,'passenger_rides':passenger_rides},RequestContext(request))

@login_required
def add_passenger(request):
    if request.method == 'POST':
        form = PassengerForm(request.POST)
        passenger = Passenger(passenger=request.user)
        if not form.is_valid():
            return render_to_response('location/add_passenger.html',{'form':form}, RequestContext(request))
        else:    
            request.user.message_set.create(message=extract(form,passenger))
            passenger.maxDelay = form.cleaned_data['maxDelay']
            passenger.seatsNeeded = form.cleaned_data['seatsNeeded']
            passenger.save()
        return HttpResponseRedirect('/location/passenger/')
    else:
        form = PassengerForm()
        return render_to_response('location/add_passenger.html',{'form':form}, RequestContext(request))

@login_required
def add_ride(request):
    if request.method == 'POST':
        form = RideForm(request.POST)
        ride = Ride(driver=request.user)
        if not form.is_valid():
            return render_to_response('location/add_ride.html',{'form':form}, RequestContext(request))
        else:    
            request.user.message_set.create(message=extract(form,ride))
            ride.driverMaxDistance = form.cleaned_data['driverMaxDistance']
            ride.driverMaxDuration = form.cleaned_data['driverMaxDuration']
            ride.freeSeats = form.cleaned_data['freeSeats']
            ride.distance = request.POST.get('distance','')
            ride.duration = request.POST.get('duration', '')
            ride.save()
        return HttpResponseRedirect('/location/ride/')
    else:
        form = RideForm()
        return render_to_response('location/add_ride.html',{'form':form}, RequestContext(request))

@user_passes_test(lambda u: u.has_perm('location.arrivals'), login_url='/news/')
def add_arrival(request):
    if request.method == 'POST':
        form = ArrivalForm(request.POST)
        if form.is_valid():
            location = Location(house_number=form.cleaned_data['house_number'],
                                street=form.cleaned_data['street'],
                                city_name=form.cleaned_data['city_name'],
                                zip_code=form.cleaned_data['zip_code'])
            location.save()
            arrival = Arrivals(location=location,name=form.cleaned_data['arr_name'])
            arrival.save()
            request.user.message_set.create(message='La destination a bien été ajoutée.')
            return HttpResponseRedirect('/location/arrivals/')
        else:
            return render_to_response('location/add_arrival.html',{'form':form},RequestContext(request))
    else:
        form = ArrivalForm()
        return render_to_response('location/add_arrival.html',{'form':form},RequestContext(request))

@login_required
def edit_passenger(request,passenger_id):
    try:
        passenger = Passenger.objects.get(pk=passenger_id)
        if request.method == 'POST':
            form = PassengerForm(request.POST)
            if not form.is_valid():
                return render_to_response('location/add_passenger.html',{'form':form, 'passenger':passenger}, RequestContext(request))
            else: 
                request.user.message_set.create(message=extract(form,passenger))
                passenger.maxDelay = form.cleaned_data['maxDelay']
                for match in passenger.ridematches_set.all() :
                    if match.accepted:
                        send_mail('Modfication du trajet d\'un passager d\'un covoiturage',u'%s, passager de votre trajet entre %s et %s a modifié ses paramètres. Vous n\'avez donc plus à aller prendre cette personne.\n Rendez vous sur http://127.0.0.1:8000/location/ride/edit/%d/ pour mettre à jour vos informations. Vous devez enregistrer les modifications afin que les renseignements concernant les distances soient mis à jour.' % (match.passenger_ride.passenger.username,match.driver_ride.start.city_name,match.driver_ride.dest,match.driver_ride.id),'nawak',[u'%s'%match.driver_ride.driver.email])
                        match.driver_ride.freeSeats = match.driver_ride.freeSeats + passenger.seatsNeeded
                        match.driver_ride.save()
                        match.driver_ride.stage_set.all().delete()
                    match.delete()
                passenger.seatsNeeded = form.cleaned_data['seatsNeeded']
                passenger.save()
                request.user.message_set.create(message='La demande de covoiturage a bien été modifiée')
            return HttpResponseRedirect('/location/ride/')
        else:
            data = pre_fill_passenger(passenger)
            form = PassengerForm(data)
            return render_to_response('location/add_passenger.html',{'form':form, 'passenger':passenger}, RequestContext(request))
    except Passenger.DoesNotExist:
        request.user.message_set.create(message='La requête de covoiturage demandée n\'existe pas')
        return HttpResponseRedirect('/location/ride/')
@login_required
def edit_ride(request, ride_id):
    try:
        ride = Ride.objects.get(pk=ride_id)
        if request.method == 'POST':
            form = RideForm(request.POST)
            if not form.is_valid():
                return render_to_response('location/add_ride.html',{'form':form, 'ride':ride}, RequestContext(request))
            else: 
                request.user.message_set.create(message=extract(form,ride))
                ride.driverMaxDistance = form.cleaned_data['driverMaxDistance']
                ride.driverMaxDuration = form.cleaned_data['driverMaxDuration']
                ride.freeSeats = form.cleaned_data['freeSeats']
                ride.distance = request.POST.get('distance','')
                ride.duration = request.POST.get('duration','')
                ride.save()
                ride.stage_set.all().delete()
                for match in ride.ridematches_set.all() :
                    send_mail('Modification d\'un covoiturage',u'Un covoiturage concernant votre trajet entre %s et %s a été modifié et donc supprimé pour éviter des informations erronées.\n Rendez vous sur http://127.0.0.1:8000/location/passenger/search/%d/ pour refaire une recherche afin de trouver de nouvelles opportunités de covoiturage' % (match.passenger_ride.start.city_name,match.passenger_ride.dest,match.passenger_ride.id),'nawak',[u'%s'%match.passenger_ride.passenger.email])
                    match.delete()
            return HttpResponseRedirect('/location/ride/')
        else:
            data = pre_fill_ride(ride)
            form = RideForm(data)
            return render_to_response('location/add_ride.html',{'form':form, 'ride':ride}, RequestContext(request))
    except Ride.DoesNotExist:
        request.user.message_set.create(message='Le trajet demandé n\'existe pas')
        return HttpResponseRedirect('/location/ride/')

@user_passes_test(lambda u: u.has_perm('location.arrivals'), login_url='/news/')
def edit_arrival(request,arrival_id):
    try:
        arrival = Arrivals.objects.get(pk=arrival_id)
        if request.method == 'POST':
            form = ArrivalForm(request.POST)
            if form.is_valid():
                arrival.location.house_number = form.cleaned_data['house_number']
                arrival.location.street = form.cleaned_data['street']
                arrival.location.city_name = form.cleaned_data['city_name']
                arrival.location.zip_code = form.cleaned_data['zip_code']
                arrival.location.save()
                destCoord = find_coordinates(arrival.location.house_number,arrival.location.street,arrival.location.zip_code,arrival.location.city_name)
                arrival.location.latitude = float(destCoord.split(",")[2])
                arrival.location.longitude = float(destCoord.split(",")[3])
                arrival.location.save()
                arrival.name = form.cleaned_data['arr_name']
                arrival.save()
                request.user.message_set.create(message='La destination a bien été modifiée')
                return HttpResponseRedirect('/location/arrivals/')
            else:
                return render_to_response('location/add_arrival.html',{'form':form},RequestContext(request))
        else:
            data = pre_fill_arrival(arrival)
            form = ArrivalForm(data)
            return render_to_response('location/add_arrival.html',{'form':form},RequestContext(request))
    except Arrivals.DoesNotExist:
        request.user.message_set.create(message='La destination demandée n\'existe pas.')
        return HttpResponseRedirect('/location/arrivals')

@login_required
def delete_passenger(request, passenger_id):
    try:
        passenger = Passenger.objects.get(pk=passenger_id)
        for match in passenger.ridematches_set.all() :
            if match.accepted:
                send_mail('Suppression du trajet d\'un passager d\'un covoiturage',u'%s, passager de votre trajet entre %s et %s a supprimé sa demande de covoiturage. Vous n\'avez donc plus à aller prendre cette personne.\n Rendez vous sur http://127.0.0.1:8000/location/ride/edit/%d/ pour mettre à jour vos informations. Vous devez enregistrer les modifications afin que les renseignements concernant les distances soient mis à jour.' % (match.passenger_ride.passenger.username,match.driver_ride.start.city_name,match.driver_ride.dest,match.driver_ride.id),'nawak',[u'%s'%match.driver_ride.driver.email])
                match.driver_ride.freeSeats = match.driver_ride.freeSeats + passenger.seatsNeeded
                match.driver_ride.save()
                match.driver_ride.stage_set.all().delete()
            match.delete()
        passenger.delete()
        request.user.message_set.create(message='La demande de covoiturage a bien été supprimée')
        return HttpResponseRedirect('/location/ride/')
    except Passenger.DoesNotExist:
        request.user.message_set.create(message='La requête de covoiturage demandée n\'existe pas')
        return HttpResponseRedirect('/location/ride/')

@login_required    
def delete_ride(request, ride_id):
    try:
        ride = Ride.objects.get(pk=ride_id)
        ride.stage_set.all().delete()
        for match in ride.ridematches_set.all() :
            send_mail('Suppression d\'un covoiturage',u'Un covoiturage concernant votre trajet entre %s et %s a été supprimé.\n Rendez vous sur http://127.0.0.1:8000/location/passenger/search/%d/ pour refaire une recherche afin de trouver de nouvelles opportunités de covoiturage' % (match.passenger_ride.start.city_name,match.passenger_ride.dest,match.passenger_ride.id),'nawak',[u'%s'%match.passenger_ride.passenger.email])
            match.delete()
        ride.delete()
        request.user.message_set.create(message='Le trajet a bien été supprimé')
        return HttpResponseRedirect('/location/ride/')
    except Passenger.DoesNotExist:
        request.user.message_set.create(message='Le trajet demandé n\'existe pas')
        return HttpResponseRedirect('/location/ride/')

@user_passes_test(lambda u: u.has_perm('location.arrivals'), login_url='/news/')
def delete_arrival(request,arrival_id):
    try:
        arrival = Arrivals.objects.get(pk=arrival_id)
        Passenger.objects.filter(dest=arrival).delete()
        Ride.objects.filter(dest=arrival).delete()
        arrival.delete()
        request.user.message_set.create(message='La destination a bien été supprimée.')
        return HttpResponseRedirect('/location/arrivals/')
    except Arrivals.DoesNotExist:
        request.user.message_set.create(message='La destination demandée n\'existe pas.')
        return HttpResponseRedirect('/location/arrivals')

@login_required
def search(request,passenger_id):
    try:
        passenger = Passenger.objects.get(pk=passenger_id)
        rides = [ride for ride in Ride.objects.select_related().filter(dest=passenger.dest,freeSeats__gte=passenger.seatsNeeded) if isPotentialDriver(ride, passenger)]
        if request.method == 'POST':
            drivers = [ride for ride in rides if request.POST.get('check%d' % ride.id) == "on" if RideMatches.objects.filter(driver_ride=ride,passenger_ride=passenger).count() == 0]
            for driver in drivers:
                match = RideMatches(driver_ride=driver,
                                    passenger_ride=passenger,
                                    newDistance=request.POST.get('dist%d' % ride.id),
                                    newDuration=request.POST.get('dur%d' % ride.id),
                                    accepted=False)
                match.save()
            return HttpResponseRedirect('/location/ride/matches')
        else:
            to_serialize = [{'start': ride.start_loc, 'driverMaxDistance': ride.driverMaxDistance, 'driverMaxDuration': ride.driverMaxDuration, 'initialDist': ride.distance, 'initialDur': ride.duration} for ride in rides]
            return render_to_response('location/matching.html',{'rides':rides,'passenger':passenger, 'json': simplejson.dumps(to_serialize)}, RequestContext(request))
    except Passenger.DoesNotExist:    
        request.user.message_set.create(message='Le trajet demandé n\'existe pas')
        return HttpResponseRedirect('/location/ride/')
@login_required
def confirm_match(request,match_id):
    try:
        match = RideMatches.objects.get(pk=match_id)
        if request.user == match.driver_ride.driver:
            match.accepted = True;
            match.save()
            ride = match.driver_ride
            ride.distance = match.newDistance
            ride.duration = match.newDuration
            ride.freeSeats -= match.passenger_ride.seatsNeeded
            ride.save()
            stage = Stage(ride=ride,location=match.passenger_ride.start,order=1)
            stage.save()
            request.user.message_set.create(message='Covoiturage confirmé.')
            send_mail(u'Covoiturage accepté par %s'%match.driver_ride.driver.username, u'%s a accepté la demande de covoiturage suivante : http://127.0.0.1:8000/location/ride/matches/%d/ .\n Veuiller prendre contact avec lui pour conclure l\'arrangement.'%(match.driver_ride.driver.username,match.id),'nawak',[u'%s'%match.passenger_ride.passenger.email])
            return HttpResponseRedirect('/location/ride/')
        else:
            request.user.message_set.create(message='Vous n\'avez pas le droit d\'accepter ce covoiturage.')
            return HttpResponseRedirect('/location/ride/matches')
    except RideMatches.DoesNotExist:
        request.user.message_set.create(message='Le covoiturage demandé n\'existe pas.')
        return HttpResponseRedirect('/location/ride/matches')

@login_required
def deny_match(request,match_id):
    try:
        match = RideMatches.objects.get(pk=match_id)
        send_mail(u'Covoiturage refusé par %s'%match.driver_ride.driver.username, u'%s a refusé la demande de covoiturage suivante : http://127.0.0.1:8000/location/passenger/%d/ .'%(match.driver_ride.driver.username,match.passenger_ride.id),'nawak',[u'%s'%match.passenger_ride.passenger.email])
        if request.user == match.driver_ride.driver:
            if match.accepted:
                match.driver_ride.freeSeats = match.driver_ride.freeSeats + match.passenger_ride.seatsNeeded
                match.driver_ride.save()
                match.driver_ride.stage_set.all().delete()
            match.delete()
            request.user.message_set.create(message='Covoiturage refusé.')
            return HttpResponseRedirect('/location/ride/matches/')
        else:
            request.user.message_set.create(message='Vous n\'avez pas le droit de refuser ce covoiturage.')
            return HttpResponseRedirect('/location/ride/matches/')
    except RideMatches.DoesNotExist:
        request.user.message_set.create(message='Le covoiturage demandé n\'existe pas.')
        return HttpResponseRedirect('/location/ride/matches')

@login_required
def cancel_match(request,match_id):
    try:
        match = RideMatches.objects.get(pk=match_id)
        if request.user == match.driver_ride.driver or request.user == match.passenger_ride.passenger:
            match.driver_ride.freeSeats = match.driver_ride.freeSeats + match.passenger_ride.seatsNeeded
            match.driver_ride.save()
            match.driver_ride.stage_set.all().delete()
            match.accepted = False
            match.save()
            send_mail('Suppression d\'un covoiturage',u'Un covoiturage concernant votre trajet entre %s et %s a été supprimé par un des deux partis.\n Rendez vous sur http://127.0.0.1:8000/location/ride/search/%d/ pour refaire une recherche afin de trouver de nouvelles opportunités de covoiturage' % (match.passenger_ride.start.city_name,match.passenger_ride.dest,match.passenger_ride.id),'nawak',[u'%s'%match.passenger_ride.passenger.email])
            send_mail('Suppression d\'un covoiturage',u'Un covoiturage concernant votre trajet entre %s et %s a été supprimé par un des deux partis. Vous n\'avez donc plus à aller prendre %s.\n Rendez vous sur http://127.0.0.1:8000/location/ride/edit/%d/ pour mettre à jour vos informations. Vous devez enregistrer les modifications afin que les renseignements concernant les distances soient mis à jour.' % (match.driver_ride.start.city_name,match.driver_ride.dest,match.passenger_ride.passenger.username,match.driver_ride.id),'nawak',[u'%s'%match.driver_ride.driver.email])
            return HttpResponseRedirect('/location/ride/matches/')
        else:
            request.user.message_set.create(message='Vous n\'avez pas le droit de supprimer ce covoiturage.')
            return HttpResponseRedirect('/location/ride/matches')
    except RideMatches.DoesNotExist:
        request.user.message_set.create(message='Le covoiturage demandé n\'existe pas.')
        return HttpResponseRedirect('/location/ride/matches')

@login_required
def show_match(request,match_id):
    try:
        match = RideMatches.objects.get(pk=match_id)
        if match.driver_ride.dateTime < match.passenger_ride.dateTime:
            startDate = match.passenger_ride.dateTime
        else:
            startDate = match.driver_ride.dateTime
        return render_to_response('location/show_match.html', {'match':match,'driver':match.driver_ride.driver,'passenger':match.passenger_ride.passenger,"startDate":startDate}, RequestContext(request))
    except RideMatches.DoesNotExist:
        request.user.message_set.create(message='Le covoiturage demandé n\'existe pas')
        return HttpResponseRedirect('/location/ride/matches')

@login_required
def show_passenger(request,passenger_id):
    try:
        passenger = Passenger.objects.get(pk=passenger_id)
        return render_to_response('location/show_passenger.html', {'passenger':passenger}, RequestContext(request))
    except Ride.DoesNotExist:
        request.user.message_set.create(message='La requête de covoiturage demandée n\'existe pas')
        return HttpResponseRedirect('/location/passenger/')

@login_required
def show_ride(request,ride_id):
    try:
        ride = Ride.objects.get(pk=ride_id)
        return render_to_response('location/show_ride.html', {'ride':ride}, RequestContext(request))
    except Ride.DoesNotExist:
        request.user.message_set.create(message='Le trajet demandé n\'existe pas')
        return HttpResponseRedirect('/location/ride/')

@login_required
def show_match_map(request,match_id):
    try:
        match = RideMatches.objects.get(pk=match_id)
        return render_to_response('location/show_match_map.html', {'match':match}, RequestContext(request))
    except RideMatches.DoesNotExist:
        request.user.message_set.create(message='Le covoiturage demandé n\'existe pas')
        return HttpResponseRedirect('/location/ride/matches')

def extract(form, ride):
    if form.is_valid():
        ride.dest = form.cleaned_data['destination']
        startCoord = find_coordinates(form.cleaned_data['start_house_number'],form.cleaned_data['start_street'],form.cleaned_data['start_zip_code'],form.cleaned_data['start_city_name'])
        destCoord = find_coordinates(ride.dest.location.house_number,ride.dest.location.street,ride.dest.location.zip_code,ride.dest.location.city_name)
        ride.dest.location.latitude = float(destCoord.split(",")[2])
        ride.dest.location.longitude = float(destCoord.split(",")[3])
        ride.dest.location.save()
        try:
            if not ride.start == None:
                ride.start.street = form.cleaned_data['start_street']
                ride.start.house_number = form.cleaned_data['start_house_number']
                ride.start.city_name = form.cleaned_data['start_city_name']
                ride.start.zip_code = form.cleaned_data['start_zip_code']
                ride.start.latitude = float(startCoord.split(",")[2])
                ride.start.longitude = float(startCoord.split(",")[3])
                ride.start.save()
        except Location.DoesNotExist:        
            start = Location(street=form.cleaned_data['start_street'],
                                house_number=form.cleaned_data['start_house_number'],
                                city_name = form.cleaned_data['start_city_name'],
                                zip_code= form.cleaned_data['start_zip_code'],
                                latitude = float(startCoord.split(",")[2]),
                                longitude= float(startCoord.split(",")[3]))
            start.save()
            ride.start = start
        ride.dateTime = datetime.combine(form.cleaned_data['date'],form.cleaned_data['time'])
        ride.everyDay = form.cleaned_data['everyDay']
        ride.save()
        return 'Vos données ont bien été modifiées'
    else:
        return 'Une erreur s\'est produite'