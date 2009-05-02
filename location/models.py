from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Location(models.Model):
    street = models.CharField(max_length=255)
    house_number = models.IntegerField(null=True)
    zip_code = models.IntegerField()
    city_name = models.CharField(max_length=255)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    def __unicode__(self):
       return "%d  %s , %s, %d" % (self.house_number, self.street, self.city_name, self.zip_code)

class Arrivals(models.Model):
    location = models.ForeignKey(Location)
    name = models.CharField(max_length=255, blank=True, null=True)
    
    def __unicode__(self):
        return "%d  %s , %s, %d" % (self.location.house_number, self.location.street, self.location.city_name, self.location.zip_code)
    class Meta:
        verbose_name_plural = "Arrivals"        



class Passenger(models.Model):
    passenger = models.ForeignKey(User)
    start = models.ForeignKey(Location,related_name = "passenger_start_location")
    dest = models.ForeignKey(Arrivals,related_name = "passenger_destination_location")
    # heure d'arrivee
    dateTime = models.DateTimeField(blank=True, null=True)
    maxDelay = models.IntegerField(blank=True,null=True)
    seatsNeeded = models.IntegerField(blank=True,null=True,default=1)
    everyDay = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "%s passager pour le trajet [%s - %s]" %(self.passenger.username,self.start.city_name,self.dest.location.city_name)
        
#Pour recuperer tous les trajets d'un user, user.ride_set.all()
# DOC many_to_one : http://www.djangoproject.com/documentation/models/many_to_one/
class Ride(models.Model):
    driver = models.ForeignKey(User)
    # heure d'arrivee
    
    dateTime = models.DateTimeField(blank=True, null=True)
    start = models.ForeignKey(Location,related_name = "driver_start_location")
    dest = models.ForeignKey(Arrivals,related_name = "driver_destination_location")
    distance = models.IntegerField(blank=True,null=True)
    duration = models.IntegerField(blank=True,null=True)
    #en km
    driverMaxDistance = models.IntegerField(blank=True,null=True)
    #en minutes
    driverMaxDuration = models.IntegerField(blank=True,null=True)
    freeSeats = models.IntegerField(blank=True,null=True)
    everyDay = models.BooleanField(default=False)
    
    @property
    def start_loc(self):
        return '%s' % self.start
    
    def __unicode__(self):
        return self.driver.username

class RideMatches(models.Model):
    driver_ride = models.ForeignKey(Ride)
    passenger_ride = models.ForeignKey(Passenger)
    newDistance = models.IntegerField()
    newDuration = models.IntegerField()
    accepted = models.BooleanField(blank=True,null=True)
    contacted = models.BooleanField(default=False,blank=True)

    def __unicode__(self):
        return "Conducteur : %s - Passager : %s " % (self.driver_ride.driver.username, self.passenger_ride.passenger.username)
        
class Stage(models.Model):
    ride = models.ForeignKey(Ride)
    location = models.ForeignKey(Location)
    order = models.IntegerField()
    
    def __unicode__(self):
        return "%s - %s : %d" %(self.ride.driver.username, self.location, self.order)

