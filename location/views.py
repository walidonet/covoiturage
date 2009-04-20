#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from datetime import datetime
from users.models import *
from location.models import *
from location.script import *
from django.template import RequestContext
from django.http import HttpResponseRedirect
from forms import RideForm, pre_fill_ride, PassengerForm, pre_fill_passenger
def search(request,passenger_id):
    try:
        passenger = Passenger.objects.get(pk=passenger_id)
        potential_rides = Ride.objects.filter(dest=passenger.dest)
        rides = []
        for ride in potential_rides:
            if isPotentialDriver(ride,passenger):
                rides.append(ride)
        return render_to_response('location/matching.html',{'rides':rides,'passenger':passenger}, RequestContext(request))
    except Passenger.DoesNotExist:    
        request.user.message_set.create(message='Le trajet demandé n\'existe pas')
        return HttpResponseRedirect('/location/ride/')

@login_required
def add_passenger(request):
    try:
        user_profile = request.user.get_profile()
        if request.method == 'POST':
            form = PassengerForm(request.POST)
            passenger = Passenger(passenger=request.user)
            if not form.is_valid():
                return render_to_response('location/add_passenger.html',{'form':form,'user_profile':user_profile}, RequestContext(request))
            else:    
                request.user.message_set.create(message=extract(form,passenger))
                passenger.maxDelay = form.cleaned_data['maxDelay']
                passenger.save()
            return HttpResponseRedirect('/location/ride/')
        else:
            form = PassengerForm()
            return render_to_response('location/add_passenger.html',{'form':form,'user_profile':user_profile}, RequestContext(request))
    except UserProfile.DoesNotExist:
        return HttpResponseRedirect('/users/profile')

@login_required    
def delete_passenger(request, passenger_id):
    try:
        passenger = Passenger.objects.get(pk=passenger_id)
        passenger.delete()
        request.user.message_set.create(message='Le trajet a bien été supprimé')
        return HttpResponseRedirect('/location/ride/')
    except Passenger.DoesNotExist:
        request.user.message_set.create(message='Le trajet demandé n\'existe pas')
        return HttpResponseRedirect('/location/ride/')
def edit_passenger(request,passenger_id):
    try:
        passenger = Passenger.objects.get(pk=passenger_id)
        user_profile = request.user.get_profile()
        if request.method == 'POST':
            form = PassengerForm(request.POST)
            if not form.is_valid():
                return render_to_response('location/add_passenger.html',{'form':form, 'passenger':passenger,'user_profile':user_profile}, RequestContext(request))
            else: 
                request.user.message_set.create(message=extract(form,passenger))
                passenger.maxDelay = form.cleaned_data['maxDelay']
                passenger.save()
            return HttpResponseRedirect('/location/ride/')
        else:
            data = pre_fill_passenger(passenger)
            form = PassengerForm(data)
            return render_to_response('location/add_passenger.html',{'form':form, 'passenger':passenger,'user_profile':user_profile}, RequestContext(request))
    except Passenger.DoesNotExist:
        request.user.message_set.create(message='Le trajet demandé n\'existe pas')
        return HttpResponseRedirect('/location/ride/')
    except UserProfile.DoesNotExist:
        return HttpResponseRedirect('/users/profile')
    
    
@login_required
def list_ride(request):
    rides = Ride.objects.filter(driver=request.user).order_by('dateTime')
    #stages = rides.stage_set.all().order_by('order')
    passengers = Passenger.objects.filter(passenger=request.user).order_by('dateTime')
    return render_to_response('location/my_rides.html',{'rides':rides,'passengers':passengers}, RequestContext(request))

@login_required
def add_ride(request):
    try:
        user_profile = request.user.get_profile()
        if request.method == 'POST':
            form = RideForm(request.POST)
            ride = Ride(driver=request.user)
            if not form.is_valid():
                return render_to_response('location/add_ride.html',{'form':form,'user_profile':user_profile}, RequestContext(request))
            else:    
                request.user.message_set.create(message=extract(form,ride))
                ride.driverMaxDistance = form.cleaned_data['driverMaxDistance']
                ride.driverMaxDuration = form.cleaned_data['driverMaxDuration']
                ride.freeSeats = form.cleaned_data['freeSeats']
                ride.distance = request.POST.get('distance','')
                ride.duration = request.POST.get('duration', '')
                ride.save()
                print getDistance(ride.start.latitude, ride.start.longitude, ride.dest.location.latitude, ride.dest.location.longitude)
            return HttpResponseRedirect('/location/ride/')
        else:
            form = RideForm()
            return render_to_response('location/add_ride.html',{'form':form,'user_profile':user_profile}, RequestContext(request))
    except UserProfile.DoesNotExist:
        return HttpResponseRedirect('/users/profile')

@login_required    
def delete_ride(request, ride_id):
    try:
        ride = Ride.objects.get(pk=ride_id)
        ride.delete()
        request.user.message_set.create(message='Le trajet a bien été supprimé')
        return HttpResponseRedirect('/location/ride/')
    except Passenger.DoesNotExist:
        request.user.message_set.create(message='Le trajet demandé n\'existe pas')
        return HttpResponseRedirect('/location/ride/')

@login_required
def edit_ride(request, ride_id):
    try:
        ride = Ride.objects.get(pk=ride_id)
        user_profile = request.user.get_profile()
        if request.method == 'POST':
            form = RideForm(request.POST)
            if not form.is_valid():
                return render_to_response('location/add_ride.html',{'form':form, 'ride':ride,'user_profile':user_profile}, RequestContext(request))
            else: 
                request.user.message_set.create(message=extract(form,ride))
                ride.driverMaxDistance = form.cleaned_data['driverMaxDistance']
                ride.driverMaxDuration = form.cleaned_data['driverMaxDuration']
                ride.freeSeats = form.cleaned_data['freeSeats']
                ride.distance = request.POST.get('distance','')
                ride.duration = request.POST.get('duration','')
                ride.save()
                print "Distance : %d" % (getDistance(ride.start.latitude, ride.start.longitude, ride.dest.location.latitude, ride.dest.location.longitude))
            return HttpResponseRedirect('/location/ride/')
        else:
            data = pre_fill_ride(ride)
            form = RideForm(data)
            return render_to_response('location/add_ride.html',{'form':form, 'ride':ride,'user_profile':user_profile}, RequestContext(request))
    except Ride.DoesNotExist:
        request.user.message_set.create(message='Le trajet demandé n\'existe pas')
        return HttpResponseRedirect('/location/ride/')
    except UserProfile.DoesNotExist:
        return HttpResponseRedirect('/users/profile')

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