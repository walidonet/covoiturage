import urllib
def find_coordinates(house_number,street,zip_code,city_name):
    query = '%d+%s,+%d,+%s,+Belgium' % (house_number,street.replace(' ','+'),zip_code,city_name.replace(' ','+'))
    url = 'http://maps.google.com/maps/geo?q=%s&output=csv&oe=utf8&sensor=true_or_false&key=your_api_key' % (query)
    print url
    return urllib.urlopen(url).read()