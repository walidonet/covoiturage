# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from models import Location, Arrivals, Ride
import datetime

class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = ('house_number', 'street', 'city_name', 'zip_code')
class ArrivalForm(forms.Form):
    house_number = forms.IntegerField()
    street = forms.CharField(max_length=255)
    city_name = forms.CharField(max_length=255)
    zip_code = forms.IntegerField()
    arr_name = forms.CharField(max_length=255)

def pre_fill_arrival(arrival):
    return {'house_number':arrival.location.house_number,
            'street':arrival.location.street,
            'city_name':arrival.location.city_name,
            'zip_code':arrival.location.zip_code,
            'arr_name':arrival.name}

class PassengerForm(forms.Form):
    date = forms.DateField(required=False,initial=datetime.date.today,help_text=u"Format : Année-Mois-Jour")
    time = forms.TimeField(required=False, initial=datetime.time, help_text=u"Format : Heure-Minute-Seconde")
    start_house_number = forms.IntegerField()
    start_street = forms.CharField(max_length=255)
    start_city_name = forms.CharField(max_length=255)
    start_zip_code = forms.IntegerField()
    destination = forms.ModelChoiceField(Arrivals.objects.all(),empty_label=None)
    maxDelay = forms.IntegerField(initial=0,help_text=u'Ce nombre correspond à la fourchette de temps dans laquelle vous acceptez d\'arrivée à destination. Si vous choisissez 10 minutes, cela signifie que vous acceptez d\'arriver 10 minutes avant ou 10 minutes après l\'heure d\'arrivée rentrée précédemment.')
    seatsNeeded = forms.IntegerField(initial=1)
    everyDay = forms.BooleanField(required=False)
    
def pre_fill_passenger(passenger):
    return {'date': passenger.dateTime.date(),
            'time': passenger.dateTime.time(),
            'start_house_number': passenger.start.house_number,
            'start_street': passenger.start.street,
            'start_city_name': passenger.start.city_name,
            'start_zip_code': passenger.start.zip_code,
            'destination': passenger.dest.id,
            'maxDelay': passenger.maxDelay,
            'seatsNeeded': passenger.seatsNeeded,
            'everyDay': passenger.everyDay}

class RideForm(forms.Form):
    date = forms.DateField(required=False,initial=datetime.date.today,help_text=u"Format : Année-Mois-Jour")
    time = forms.TimeField(required=False,initial=datetime.time, help_text=u"Format : Heure-Minute-Seconde")
    start_house_number = forms.IntegerField()
    start_street = forms.CharField(max_length=255)
    start_city_name = forms.CharField(max_length=255)
    start_zip_code = forms.IntegerField()
    destination = forms.ModelChoiceField(Arrivals.objects.all(),empty_label=None)
    driverMaxDistance = forms.IntegerField(initial=0,help_text=u"Ce nombre correspond à la distance maximale du détour en Km que vous acceptez de parcourir pour prendre une personne")
    driverMaxDuration = forms.IntegerField(initial=0,help_text=u"Ce nombre correspond à la durée maximale du détour en minutes que vous acceptez pour prendre une personne")
    freeSeats = forms.IntegerField(initial=0)
    everyDay = forms.BooleanField(required=False)
    distance = forms.IntegerField(initial=0,required=False,widget=forms.HiddenInput)
    duration = forms.IntegerField(initial=0,required=False,widget=forms.HiddenInput)

def pre_fill_ride(ride):
    return {'date': ride.dateTime.date(),
            'time': ride.dateTime.time(),
            'start_house_number': ride.start.house_number,
            'start_street': ride.start.street,
            'start_city_name': ride.start.city_name,
            'start_zip_code': ride.start.zip_code,
            'destination': ride.dest.id,
            'driverMaxDistance': ride.driverMaxDistance,
            'driverMaxDuration': ride.driverMaxDuration,
            'freeSeats': ride.freeSeats,
            'everyDay': ride.everyDay}
            
# 'dest_house_number': ride.dest.location.house_number,
#             'dest_street': ride.dest.location.street,
#             'dest_city_name': ride.dest.location.city_name,
#             'dest_zip_code': ride.dest.location.zip_code,
#            'destination' : ride.dest.,