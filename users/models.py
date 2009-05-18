from django.db import models
from django.contrib.auth.models import User
from location.models import Location

class Config(models.Model):
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=255)
    
    def __unicode__(self):
        return "%s -> %s" % (self.key, self.value)

class Photo(models.Model):
    user = models.ForeignKey(User, unique=True)
    #photo = models.ImageField(upload_to='user_pics')
    extension = models.CharField(max_length=10)
    
    def __unicode__(self):
        return "%s%s" % (self.user.username,self.extension)

class PhoneNumber(models.Model):
    user = models.ForeignKey(User)
    number = models.CharField(max_length=10)

    def __unicode__(self):
        return "%s" % self.number
class Address(models.Model):
    user = models.ForeignKey(User)
    location = models.ForeignKey(Location)
    
    def __unicode__(self):
        return "%s" % self.location

class Favorites(models.Model):
    user = models.ForeignKey(User, related_name = "favorites_owner")
    favorite = models.ForeignKey(User, related_name = "favorites_member")
    #pour recup les favoris d'un utilisateur, utiliser user.favorites_owner.all()
    def __unicode__(self):
        return "%s - %s" % (self.user.username,self.favorite.username)
        