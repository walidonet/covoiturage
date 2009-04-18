from django import forms

class UserForm(forms.Form):
    phone_number = forms.CharField(max_length=9,required=False)
    mobile_phone_number = forms.CharField(max_length=10,required=False)
    house_number = forms.IntegerField()
    street = forms.CharField(max_length=255)
    city_name = forms.CharField(max_length=255)
    zip_code = forms.IntegerField()

def pre_fill(profile):
    return {'phone_number': profile.phone_number,
            'mobile_phone_number': profile.mobile_phone_number,
            'house_number': profile.location.house_number,
            'street': profile.location.street,
            'city_name': profile.location.city_name,
            'zip_code': profile.location.zip_code}