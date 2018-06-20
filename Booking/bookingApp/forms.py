from django import forms
from .models import IncludedService

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
    
class registrationForm(forms.Form):
    nome = forms.CharField(max_length=50, required=True)
    surname = forms.CharField(max_length=50, required=True)
    birthday = forms.DateField(required=True)
    cf = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(max_length=100, required=True)
    street = forms.CharField(max_length=100, required=True)
    houseNumber = forms.IntegerField(required=True)
    city = forms.CharField(max_length=30, required=True)
    zipCode = forms.CharField(max_length=15, required=True)