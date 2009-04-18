#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from users.models import *
from location.models import *
from location.script import *
from django.template import RequestContext
from django.http import HttpResponseRedirect
from forms import RideForm, pre_fill_ride

@login_required
def list_ride(request):
    rides = Ride.objects.filter(driver=request.user).order_by('date')
    #stages = rides.stage_set.all().order_by('order')
    passengers = Passenger.objects.filter(passenger=request.user).order_by('date')
    return render_to_response('location/my_rides.html',{'rides':rides,'passengers':passengers}, RequestContext(request))

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
                ride.distance = request.POST.get('distance','')
                ride.duration = request.POST.get('duration', '')
                ride.save()
            return HttpResponseRedirect('/location/ride/')
        else:
            form = RideForm()
            return render_to_response('location/add_ride.html',{'form':form,'user_profile':user_profile}, RequestContext(request))
    except UserProfile.DoesNotExist:
        return HttpResponseRedirect('/users/profile')
def delete_ride(request, ride_id):
    try:
        ride = Ride.objects.get(pk=ride_id)
        ride.delete()
        request.user.message_set.create(message='Le trajet a bien été supprimé')
        return HttpResponseRedirect('/location/ride/')
    except News.DoesNotExist:
        request.user.message_set.create(message='Le trajet demandé n\'existe pas')
        return HttpResponseRedirect('/location/ride/')
        
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
                ride.distance = request.POST.get('distance','')
                ride.duration = request.POST.get('duration','')
                ride.save()
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
        startCoord = find_coordinates(form.cleaned_data['start_house_number'],form.cleaned_data['start_street'],form.cleaned_data['start_zip_code'],form.cleaned_data['start_city_name'])
        destCoord = find_coordinates(form.cleaned_data['dest_house_number'],form.cleaned_data['dest_street'],form.cleaned_data['dest_zip_code'],form.cleaned_data['dest_city_name'])
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
        try:
            if not ride.dest == None:
                ride.dest.location.street = form.cleaned_data['dest_street']
                ride.dest.location.house_number = form.cleaned_data['dest_house_number']
                ride.dest.location.city_name = form.cleaned_data['dest_city_name']
                ride.dest.location.zip_code = form.cleaned_data['dest_zip_code']
                ride.dest.location.latitude = float(destCoord.split(",")[2])
                ride.dest.location.longitude = float(destCoord.split(",")[3])
                ride.dest.location.save()
                ride.dest.save()
        except Arrivals.DoesNotExist:        
            dest = Location(street=form.cleaned_data['dest_street'],
                                house_number=form.cleaned_data['dest_house_number'],
                                city_name = form.cleaned_data['dest_city_name'],
                                zip_code= form.cleaned_data['dest_zip_code'],
                                latitude = float(destCoord.split(",")[2]),
                                longitude= float(destCoord.split(",")[3]))
            dest.save()
            arr = Arrivals(location=dest,name='')
            arr.save()
            ride.dest = arr
        ride.duration
        ride.date = form.cleaned_data['date']
        ride.time = form.cleaned_data['time']
        ride.driverMaxDistance = form.cleaned_data['driverMaxDistance']
        ride.driverMaxDuration = form.cleaned_data['driverMaxDuration']
        ride.freeSeats = form.cleaned_data['freeSeats']
        ride.everyDay = form.cleaned_data['everyDay']
        ride.save()
        return 'Vos données ont bien été modifiées'
    else:
        return 'Une erreur s\'est produite'