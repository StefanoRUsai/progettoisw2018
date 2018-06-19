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
    services = forms.MultipleChoiceField(choices=IncludedService.availableServices, widget=forms.CheckboxSelectMultiple(attr={"class": "form-control"}))
    price = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
