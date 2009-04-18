from math import *
import urllib

def find_coordinates(house_number,street,zip_code,city_name):
    query = '%d+%s,+%d,+%s,+Belgium' % (house_number,street.replace(' ','+'),zip_code,city_name.replace(' ','+'))
    url = 'http://maps.google.com/maps/geo?q=%s&output=csv&oe=utf8&sensor=true_or_false&key=your_api_key' % (query)
    return urllib.urlopen(url).read()

#def find_coordinates(loc):
#    return find_coordinates(loc.house_number,loc.street,loc.zip_code,loc.city_name)

def getDistance(lat1, lon1, lat2, lon2):
    r = 6371
    deltaLat = radians(lat2 - lat1)
    deltaLon = radians(lon2 - lon1)
    a = pow(sin(deltaLat/2),2) + (cos(radians(lat1))*cos(radians(lat2))*pow(sin(deltaLon/2),2))
    c = 2*atan2(sqrt(a),sqrt(1-a))
    return ceil(r*c)

#def getDistance(loc1, loc2):
#    return getDistance(loc1.latitude,loc1.longitude,loc2.latitude,loc2.longitude)

def belongsToEllipse(startLat, startLon, endLat, endLon, stageLat, stageLon, driverMaxDist):
    distSE = getDistance(startLat,startLon, endLat, endLon)
    focalAxisLength = distSE + driverMaxDist
    distSStage = getDistance(startLat,startLon,stageLat,stageLon)
    distEStage = getDistance(stageLat,stageLon,endLat,endLon)
    return (distSStage + distEStage) <= focalAxisLength
    
def test():
    print belongsToEllipse(40,40,42,42,41,41,20)
    print belongsToEllipse(40,40,42,42,43,43,20)