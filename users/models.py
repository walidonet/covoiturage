from django.db import models
from django.contrib.auth.models import User
from covoiturage.location.models import Location

class UserProfile(models.Model):
    # Field required to match a user and his profile 
    # (i.e extra-fields than the ones provided by the authentication app)
    user = models.ForeignKey(User, unique=True)
    #photo = models.ImageField(upload_to='user_pics',blank=True,null=True)
    # Extra-Fields
    location = models.ForeignKey(Location, related_name="location1")
    location2 = models.ForeignKey(Location,related_name="location2",blank=True,null=True) 
    location3 = models.ForeignKey(Location,related_name="location3",blank=True,null=True) 
    
    phone_number1 = models.CharField(max_length=10)
    phone_number2 = models.CharField(max_length=10,blank=True,null=True)
    phone_number3 = models.CharField(max_length=10,blank=True,null=True)
    
    def __unicode__(self):
        return self.user.username

class Favorites(models.Model):
    user = models.ForeignKey(User, related_name = "favorites_owner")
    favorite = models.ForeignKey(User, related_name = "favorites_member")
    #pour recup les favoris d'un utilisateur, utiliser user.favorites_owner.all()
    def __unicode__(self):
        return "%s - %s" % (self.user.username,self.favorite.username)
        