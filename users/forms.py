from django import forms

class MailForm(forms.Form):
    email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=255,required=True)
    message = forms.CharField(widget=forms.Textarea,required=True)

class PhoneForm(forms.Form):
    phone = forms.CharField(max_length=10)

def pre_fill_phone(phone):
    return {'phone':phone.number}
    
class AddressForm(forms.Form):
    house_number = forms.IntegerField()
    street = forms.CharField(max_length=255)
    city_name = forms.CharField(max_length=255)
    zip_code = forms.IntegerField()

def pre_fill_address(address):
    return {'house_number':address.location.house_number,
            'street':address.location.street,
            'city_name':address.location.city_name,
            'zip_code':address.location.zip_code}

class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=255,required=False)
    last_name = forms.CharField(max_length=255,required=False)
    email = forms.EmailField(required=False)

def pre_fill_profile(user):
    return {'first_name':user.first_name,
            'last_name':user.last_name,
            'email':user.email}

class PhotoForm(forms.Form):
    photo = forms.FileField()