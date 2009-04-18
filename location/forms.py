from django import forms
from django.forms import ModelForm
from models import Location
import datetime

class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = ('house_number', 'street', 'city_name', 'zip_code')


class RideForm(forms.Form):
    date = forms.DateField(required=False,initial=datetime.date.today)
    time = forms.TimeField(required=False,initial=datetime.time)
    start_house_number = forms.IntegerField()
    start_street = forms.CharField(max_length=255)
    start_city_name = forms.CharField(max_length=255)
    start_zip_code = forms.IntegerField()
    dest_house_number = forms.IntegerField()
    dest_street = forms.CharField(max_length=255)
    dest_city_name = forms.CharField(max_length=255)
    dest_zip_code = forms.IntegerField()
    driverMaxDistance = forms.IntegerField(initial=0)
    driverMaxDuration = forms.IntegerField(initial=0)
    freeSeats = forms.IntegerField(initial=0)
    everyDay = forms.BooleanField(required=False)
    distance = forms.IntegerField(initial=0,required=False,widget=forms.HiddenInput)
    duration = forms.IntegerField(initial=0,required=False,widget=forms.HiddenInput)
    
def pre_fill_ride(ride):
    return {'date': ride.date,
            'time': ride.time,
            'start_house_number': ride.start.house_number,
            'start_street': ride.start.street,
            'start_city_name': ride.start.city_name,
            'start_zip_code': ride.start.zip_code,
            'dest_house_number': ride.dest.location.house_number,
            'dest_street': ride.dest.location.street,
            'dest_city_name': ride.dest.location.city_name,
            'dest_zip_code': ride.dest.location.zip_code,
            'driverMaxDistance': ride.driverMaxDistance,
            'driverMaxDuration': ride.driverMaxDuration,
            'freeSeats': ride.freeSeats,
            'everyDay': ride.everyDay}