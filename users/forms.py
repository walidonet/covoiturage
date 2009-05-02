from django import forms

def pre_fill(profile):
    data = {'phone_number1': profile.phone_number1,
            'phone_number2': profile.phone_number2,
            'phone_number3': profile.phone_number3,
            'loc1_house_number': profile.location.house_number,
            'loc1_street': profile.location.street,
            'loc1_city_name': profile.location.city_name,
            'loc1_zip_code': profile.location.zip_code}
    if not profile.location2 == None:
        data['loc2_house_number'] = profile.location2.house_number
        data['loc2_street'] = profile.location2.street
        data['loc2_city_name'] = profile.location2.city_name
        data['loc2_zip_code'] = profile.location2.zip_code
    if not profile.location3 == None:
        data['loc3_house_number'] = profile.location3.house_number
        data['loc3_street'] = profile.location3.street
        data['loc3_city_name'] = profile.location3.city_name
        data['loc3_zip_code'] = profile.location3.zip_code
    return data
class MailForm(forms.Form):
    email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=255,required=True)
    message = forms.CharField(widget=forms.Textarea,required=True)

class ProfileForm(forms.Form):
    loc1_house_number = forms.IntegerField(required=True)
    loc1_street = forms.CharField(max_length=255,required=True)
    loc1_city_name = forms.CharField(max_length=255,required=True)
    loc1_zip_code = forms.IntegerField(required=True)

    loc2_house_number = forms.IntegerField(required=False)
    loc2_street = forms.CharField(max_length=255,required=False)
    loc2_city_name = forms.CharField(max_length=255,required=False)
    loc2_zip_code = forms.IntegerField(required=False)

    loc3_house_number = forms.IntegerField(required=False)
    loc3_street = forms.CharField(max_length=255,required=False)
    loc3_city_name = forms.CharField(max_length=255,required=False)
    loc3_zip_code = forms.IntegerField(required=False)

    phone_number1 = forms.CharField(max_length=10)
    phone_number2 = forms.CharField(max_length=10,required=False)
    phone_number3 = forms.CharField(max_length=10,required=False)
    