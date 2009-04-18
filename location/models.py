from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Location(models.Model):
    street = models.CharField(max_length=255)
    house_number = models.IntegerField(null=True)
    zip_code = models.IntegerField()
    city_name = models.CharField(max_length=255)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    def __unicode__(self):
        return  "%s , %s - %d, %s" % (self.house_number, self.street, self.zip_code, self.city_name)
#ecrire methode update coordinates en fonction du callback

class Arrivals(models.Model):
    location = models.ForeignKey(Location)
    name = models.CharField(max_length=255, blank=True, null=True)
    
    def __unicode__(self):
        if not self.name == '':
            return self.name
        else:
            return "%s" % (self.location.__unicode__())
    class Meta:
        verbose_name_plural = "Arrivals"        

class Passenger(models.Model):
    passenger = models.ForeignKey(User)
    start = models.ForeignKey(Location,related_name = "passenger_start_location")
    dest = models.ForeignKey(Arrivals,related_name = "passenger_destination_location")
    date = models.DateField(blank=True,null=True)
    #l'heure d'arrivee
    time = models.TimeField(blank=True,null=True)
    everyDay = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "%s passager pour le trajet [%s - %s]" %(self.user.username,self.start.city_name,self.dest.city_name)
        
#Pour recuperer tous les trajets d'un user, user.ride_set.all()
# DOC many_to_one : http://www.djangoproject.com/documentation/models/many_to_one/
class Ride(models.Model):
    driver = models.ForeignKey(User)
    date = models.DateField(blank=True,null=True)
    #l'heure d'arrivee
    time = models.TimeField(blank=True,null=True)
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
    
    def __unicode__(self):
        return self.driver.username

class Stage(models.Model):
    ride = models.ForeignKey(Ride)
    location = models.ForeignKey(Location)
    order = models.IntegerField()
    
    def __unicode__(self):
        return "%s - %s : %s" %(self.ride.driver.username, self.location)

