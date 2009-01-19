from django.db import models
from django.contrib.auth.models import User
#from covoiturage.location.models import Location, Address

class UserProfile(models.Model):
    # Field required to match a user and his profile 
    # (i.e extra-fields than the ones provided by the authentication app)
    user = models.ForeignKey(User, unique=True)
    
    # Extra-Fields
    #address = models.ForeignKey(Address)
    phone_number = models.CharField(max_length=9)
    mobile_phone_number = models.CharField(max_length=10)