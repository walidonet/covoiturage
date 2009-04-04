from math import *

def getDistance(lat1, lon1, lat2, lon2):
    r = 6371
    deltaLat = radians(lat2 - lat1)
    deltaLon = radians(lon2 - lon1)
    a = pow(sin(deltaLat/2),2) + (cos(radians(lat1))*cos(radians(lat2))*pow(sin(deltaLon/2),2))
    c = 2*atan2(sqrt(a),sqrt(1-a))
    return ceil(r*c)
