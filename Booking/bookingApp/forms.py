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
    roomNumber = forms.CharField(label="Room number",widget=forms.TextInput(attrs={"class": "form-control"}))
    bedsNumber = forms.CharField(label="Capacity",widget=forms.TextInput(attrs={"class": "form-control"}))
    OPTIONS = (
                  ("TELEPHONE",'TELEPHONE'),
                  ("GARAGE",'GARAGE'),
                  ("WIFI",'WIFI'),
                  ("BREAKFAST",'BREAKFAST'),
                  ("LUNCH",'LUNCH'),
                  ("DINNER",'DINNER'),
                  ("BRUNCH",'BRUNCH')
    )
    services = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={"name": "select_0","class": "fff"}),choices=OPTIONS)
    price = forms.CharField(label="Price",widget=forms.TextInput(attrs={"class": "form-control"}))

class formLogin(forms.Form):
    username = forms.CharField( required=True, widget=forms.TextInput(attrs={"class" : "form-control"}))
    password = forms.CharField( widget=forms.TextInput(attrs={'required': 'Please verify password', "class" : "form-control"}))

    def clean_username(self):
        username = self.cleaned_data["username"]
        if (RegisteredUser.objects.filter(userName=username).exists()) or (
        HotelKeeper.objects.filter(userName=username).exists()):
            return username
        else:
            raise forms.ValidationError('Username not exists')


class RegistrationForm(forms.Form):

    hotelKeeper = forms.BooleanField(widget=forms.CheckboxInput(attrs={}), required=False)
    name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    surname = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    birthday = forms.DateField(required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    cf = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(max_length=100, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    userName = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    verificapassword = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    street = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    civicNumber = forms.IntegerField(required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    city = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    zipCode = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))

    def clean_userName(self):
        username = self.cleaned_data["userName"]
        if (RegisteredUser.objects.filter(userName=username).exists()) or (
        HotelKeeper.objects.filter(userName=username).exists()):
            raise forms.ValidationError('Username exists')
        else:
            return username

    def clean_verificapassword(self):
        if self.cleaned_data["verificapassword"] != self.cleaned_data["password"]:
             raise forms.ValidationError('Verify password wrong')
        return self.cleaned_data["verificapassword"]



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
