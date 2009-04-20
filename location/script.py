# -*- coding: utf-8 -*-
from math import *
import urllib

def find_coordinates(house_number,street,zip_code,city_name):
    query = '%d+%s,+%d,+%s,+Belgium' % (house_number,street.replace(' ','+'),zip_code,city_name.replace(' ','+'))
    url = 'http://maps.google.com/maps/geo?q=%s&output=csv&oe=utf8&sensor=true_or_false&key=your_api_key' % (query)
    return urllib.urlopen(url).read()

def getDistance(lat1, lon1, lat2, lon2):
    r = 6371
    deltaLat = radians(lat2 - lat1)
    deltaLon = radians(lon2 - lon1)
    a = pow(sin(deltaLat/2),2) + (cos(radians(lat1))*cos(radians(lat2))*pow(sin(deltaLon/2),2))
    c = 2*atan2(sqrt(a),sqrt(1-a))
    return ceil(r*c)


def isPotentialDriver(ride, passenger):
    date = (ride.dateTime.date() == passenger.dateTime.date()) | ride.everyDay
    if  ride.dateTime.time() < passenger.dateTime.time():
        timedelta = passenger.dateTime - ride.dateTime
    else:
        timedelta = ride.dateTime - passenger.dateTime
    time = timedelta.seconds/60.0 <= passenger.maxDelay
    return date & time & belongsToEllipse(ride.start.latitude, ride.start.longitude,ride.dest.location.latitude,ride.dest.location.longitude,passenger.start.latitude,passenger.start.longitude, ride.driverMaxDistance)


def belongsToEllipse(startLat, startLon, endLat, endLon, stageLat, stageLon, driverMaxDist):
    distSE = getDistance(startLat,startLon, endLat, endLon)
    # *1.8 parce que ce sont des distances à vol d'oiseau et il faut compenser le trajet normal
    focalAxisLength = distSE*1.8 + driverMaxDist
    distSStage = getDistance(startLat,startLon,stageLat,stageLon)
    distEStage = getDistance(stageLat,stageLon,endLat,endLon)
    return (distSStage + distEStage) <= focalAxisLength
    
def test():
    print belongsToEllipse(40,40,42,42,41,41,20)
    print belongsToEllipse(40,40,42,42,43,43,20)