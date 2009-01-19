from django.db import models
from django.contrib.auth.models import User
STAGE_CHOICES = (
    ('Start', 'Depart'),
    ('Stage', 'Etape'),
    ('Arrival','Arrivee'),
)

# Create your models here.
class Location(models.Model):
    zip_code = models.IntegerField()
    city_name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    def __unicode__(self):
        return  self.city_name

class Address(models.Model):
    street = models.CharField(max_length=60)
    number = models.IntegerField()
    location = models.ForeignKey(Location)
    
    def __unicode__(self):
        return "%d ,%s" % (self.number,self.street,)

class Ride(models.Model):
    user = models.ForeignKey(User)
    date = models.DateTimeField()

    def __unicode__(self):
        return self.date

class Stage(models.Model):
    ride = models.ForeignKey(Ride)
    address = models.ForeignKey(Address)
    stage_type = models.CharField(max_length=7, choices=STAGE_CHOICES)
    time = models.TimeField()
    
    def __unicode__(self):
        return "%s : %s" %(self.stage_type,self.address,)

