from location.models import Arrivals,Location
from django.contrib import admin

class ArrivalsAdmin(admin.ModelAdmin):
	model = Arrivals

admin.site.register(Arrivals ,ArrivalsAdmin)

class LocationAdmin(admin.ModelAdmin):
	model = Location

admin.site.register(Location ,LocationAdmin)