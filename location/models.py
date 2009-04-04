from django.db import models
from django.contrib.auth.models import User

STAGE_CHOICES = (
    ('Start', 'Depart'),
    ('Stage', 'Etape'),
    ('Arrival','Arrivee'),
)

# Create your models here.
class Location(models.Model):
    street = models.CharField(max_length=255)
    house_number = models.IntegerField()
    zip_code = models.IntegerField()
    city_name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __unicode__(self):
        return  "%s , %s - %d, %s" % (self.house_number, self.street, self.zip_code, self.city_name)
#ecrire methode update coordinates en fonction du callback
class Ride(models.Model):
    user = models.ForeignKey(User)
    date = models.DateTimeField()

    def __unicode__(self):
        return self.date

class Stage(models.Model):
    ride = models.ForeignKey(Ride)
    location = models.ForeignKey(Location)
    stage_type = models.CharField(max_length=7, choices=STAGE_CHOICES)
    time = models.TimeField()
    
    def __unicode__(self):
        return "%s - %s : %s" %(self.ride.user.username, self.stage_type, self.location)

