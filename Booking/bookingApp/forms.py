from django import forms
from .models import *

class AddHotelForm (forms.Form):
    #maxdimensione, requisito necessario, adattamento html ni
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    description = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    street = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    houseNumber = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    city = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    zipCode = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    photoUrl = forms.ImageField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))

class AddRoomForm (forms.Form):
    roomNumber = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    bedsNumber = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    services = forms.MultipleChoiceField()
    price = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))

class formLogin(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class" : "form-control"}))
    password = forms.CharField(widget=forms.TextInput(attrs={"class" : "form-control"}))

class RegistrationForm(forms.Form):
    hotelKeeper = forms.BooleanField(widget=forms.CheckboxInput(attrs={}), required=False)
    name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    surname = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    birthday = forms.DateField(required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    cf = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(max_length=100, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    userName = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    verifyPassword = forms.CharField(label='Verify Password',max_length=50, error_messages={'required': 'Please verify password'}, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    street = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    civicNumber = forms.IntegerField(required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    city = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    zipCode = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))

    def clean_userName(self):
        userName = self.cleaned_data["userName"]
        if RegisteredUser.objects.filter(userName=userName).exists() or HotelKeeper.objects.filter(userName=userName).exists():
            raise forms.ValidationError('Username already exists')
        return userName


class PaymentForm(forms.Form):
    name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    surname = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    birthday = forms.DateField(required=True, widget=forms.DateInput(attrs={"class": "form-control"}))
    cf = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(max_length=100, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    street = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    civicNumber = forms.IntegerField(required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    city = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    zipCode = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    cardNumber = forms.CharField(min_length=15, max_length=15, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    month = forms.CharField(min_length=2, max_length=2, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    year = forms.CharField(min_length=4, max_length=4, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    cvv = forms.CharField(min_length=3, max_length=3, required=True,  widget=forms.TextInput(attrs={"class": "form-control"}))


class creditCard(forms.Form):
    cardNumber = forms.CharField(min_length=15, max_length=15, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    month = forms.CharField(min_length=2, max_length=2, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    year = forms.CharField(min_length=4, max_length=4, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    cvv = forms.CharField(min_length=3, max_length=3, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))

