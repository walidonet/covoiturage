from django import forms

class UserForm(forms.Form):
    phone_number = forms.CharField(max_length=9,required=False)
    mobile_phone_number = forms.CharField(max_length=10,required=False)
    house_number = forms.IntegerField()
    street = forms.CharField(max_length=255)
    city_name = forms.CharField(max_length=255)
    zip_code = forms.IntegerField()