from django.db.models import Q
from location.models import Ride, Passenger
from datetime import datetime
def rides(request):
    if hasattr(request, 'user'):
        user = request.user
        rides = Ride.objects.filter(Q(dateTime__gte=datetime.today().date()) | Q(everyDay=True),driver=user,).order_by('dateTime')[:1]
        passengers = Passenger.objects.filter(Q(dateTime__gte=datetime.today().date()) | Q(everyDay=True),passenger=user).order_by('dateTime')[:1]
        return {
            'rides_for_right': rides,
            'passengers_for_right': passengers,
        }
    else:
        t = ''
        return {
            'rides_for_right': t,
            'passengers_for_right': t,
        }
