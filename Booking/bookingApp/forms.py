from django import forms
from .models import *
from passlib.hash import pbkdf2_sha256


class AddHotelForm (forms.Form):
    """ classe AddHotelForm, ogni attributo di questa classe rappresenta un campo di un form
    nel template dove viene mostrato. Questo avviene tramite l'estensione della classe Form
    della libreria django"""

    name = forms.CharField(label="Name",widget=forms.TextInput(attrs={"placeholder": "Name", "class": "form-control"}))
    description = forms.CharField(label="Description",widget=forms.TextInput(attrs={"placeholder": "Description", "class": "form-control"}))
    street = forms.CharField(label="Street",widget=forms.TextInput(attrs={"placeholder": "Street", "class": "form-control"}))
    houseNumber = forms.CharField(label="N",widget=forms.NumberInput(attrs={"placeholder": "12 (example)", "class": "form-control"}))
    city = forms.CharField(label="City",widget=forms.TextInput(attrs={"placeholder": "City", "class": "form-control"}))
    zipCode = forms.CharField(label="Zip code",widget=forms.TextInput(attrs={"placeholder": "09100 (example)", "class": "form-control"}))
    photoUrl = forms.CharField(label="Photo",required=False, widget=forms.TextInput(attrs={"placeholder": "Url", "class": "form-control"}))


class AddRoomForm (forms.Form):
    """ classe AddRoomForm, ogni attributo di questa classe rappresenta un campo di un form
    nel template dove viene mostrato. Questo avviene tramite l'estensione della classe Form
    della libreria django"""

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
    services = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple,choices=OPTIONS)
    price = forms.CharField(label="Price",widget=forms.TextInput(attrs={"class": "form-control"}))


class LoginForm(forms.Form):
    """ classe LoginForm, ogni attributo di questa classe rappresenta un campo di un form
    nel template dove viene mostrato. Questo avviene tramite l'estensione della classe Form
    della libreria django"""

    username = forms.CharField( required=True, widget=forms.TextInput(attrs={"placeholder": "Username", "class" : "form-control"}))
    password = forms.CharField( widget=forms.PasswordInput(attrs={"placeholder": "Password", 'required': 'Please verify password', "class" : "form-control"}))

    def clean_username(self):
        """override del metodo clean_data del campo username, utilizzando la prassi di django, avviene un controllo sull'esistenza nel DB
        della presenza del nome scritto dall'utentem se non è presente viene sollevata un'eccezione"""
        username = self.cleaned_data["username"]
        if (RegisteredClient.objects.filter(username=username).exists()) or (
        HotelKeeper.objects.filter(username=username).exists()):
            return username
        else:
            raise forms.ValidationError('Username not exists')

    def clean_password(self):
        """override del metodo clean_data del campo password, utilizzando la prassi di django,
        si controlla se la password passata corrisponde a quella presente sul DB"""

        passCrypted = False

        #se l'username esiste nella Tabella registered client, si estraggono i dati del cliente
        if (RegisteredClient.objects.filter(username=self.cleaned_data["username"]).exists()):
            user = RegisteredClient.objects.get(username=self.cleaned_data["username"])
        # se l'username esiste nella Tabella registered client, si estraggono i dati dell'albergatore
        elif (HotelKeeper.objects.filter(username=self.cleaned_data["username"]).exists()):
            user = HotelKeeper.objects.get(username=self.cleaned_data["username"])
        # se l'username non è sul DB viene sollevate un'eccezione
        else:
            raise forms.ValidationError('User not exist')

        #verifica che la password sia criptata o no
        if list(user.password)[0] == '$':
            #assegno un valore True nel caso la password criptata sia uguale a quella criptata sul DB
            passCrypted = pbkdf2_sha256.verify(str(self.cleaned_data["password"]), user.password)
        else:
            #assegno un valore True nel caso la password non criptata sia uguale a quella sul DB (non criptata)
            if(str(self.cleaned_data["password"])==user.password):
                passCrypted = True

        if passCrypted:
            password = user.password
        else:
            raise forms.ValidationError('Wrong password')

        return password


class RegistrationForm(forms.Form):
    """ classe RegistrationForm, ogni attributo di questa classe rappresenta un campo di un form
    nel template dove viene mostrato. Questo avviene tramite l'estensione della classe Form
    della libreria django"""

    hotelKeeper = forms.BooleanField(widget=forms.CheckboxInput(attrs={}), required=False)
    name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={"placeholder": "Name", "class": "form-control"}))
    surname = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={"placeholder": "Surname", "class": "form-control"}))
    birthday = forms.DateField(required=True, widget=forms.TextInput(attrs={"placeholder": "YEAR-MONTH-DAY (1990-10-11)","class": "form-control"}))
    cf = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={"placeholder": "CFNMTT90A10B354E (example)", "class": "form-control"}))
    email = forms.EmailField(max_length=100, required=True, widget=forms.TextInput(attrs={"placeholder": "email@gmail.com (example)", "class": "form-control"}))
    username = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={"placeholder": "Username", "class": "form-control"}))
    password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={"placeholder": "Password", "class": "form-control"}))
    verifyPassword = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={"placeholder": "Verifiched Password", "class": "form-control"}))
    street = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={"placeholder": "Street", "class": "form-control"}))
    civicNumber = forms.IntegerField(required=True, widget=forms.TextInput(attrs={"placeholder": "12 (example)", "class": "form-control"}))
    city = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={"placeholder": "City", "class": "form-control"}))
    zipCode = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={"placeholder": "09100 (example)", "class": "form-control"}))


    def clean_username(self):
        """override del metodo clean_data del campo username, utilizzando la prassi di django, avviene un controllo
        sull'esistenza nel DB della presenza del nome scritto dall'utente, se si viene sollevata l'eccezione sul nome gia esistente"""

        username = self.cleaned_data["username"]
        if (RegisteredClient.objects.filter(username=username).exists()) or (
        HotelKeeper.objects.filter(username=username).exists()):
            raise forms.ValidationError('Username exists')
        else:
            return username

    def clean_verifyPassword(self):
        """override del metodo clean_data del campo verify password, utilizzando la prassi di django, se la password
        è uguale a quella inserita su verify passoword, la password viene criptata e passata per essere
        salvata sul DB, se no viene sollevata eccezione"""

        if self.cleaned_data["verifyPassword"] != self.cleaned_data["password"]:
             raise forms.ValidationError('Verify password wrong')
        #metodo per criptare la password a 256bit
        passCrypted = pbkdf2_sha256.encrypt(self.cleaned_data["verifyPassword"], rounds=12000, salt_size=32)
        return passCrypted


class PaymentForm(forms.Form):
    """ classe PaymentForm, ogni attributo di questa classe rappresenta un campo di un form
    nel template dove viene mostrato. Questo avviene tramite l'estensione della classe Form
    della libreria django"""

    name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={"placeholder": "Name", "class": "form-control"}))
    surname = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={"placeholder": "Surname", "class": "form-control"}))
    birthday = forms.DateField(required=True, widget=forms.DateInput(attrs={"placeholder": "YEAR-MONTH-DAY (1990-10-11)", "class": "form-control"}))
    cf = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={"placeholder": "CFNMTT90A10B354E (example)", "class": "form-control"}))
    email = forms.EmailField(max_length=100, required=True, widget=forms.TextInput(attrs={"placeholder": "CFNMTT90A10B354E (example)","class": "form-control"}))
    street = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={"placeholder": "Street", "class": "form-control"}))
    civicNumber = forms.IntegerField(required=True, widget=forms.TextInput(attrs={"placeholder": "12 (example)","class": "form-control"}))
    city = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={"placeholder": "City", "class": "form-control"}))
    zipCode = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={"placeholder": "09100 (example)", "class": "form-control"}))
    cardNumber = forms.CharField(min_length=15, max_length=15, required=True, widget=forms.TextInput(attrs={"placeholder": "Your card number", "class": "form-control"}))
    month = forms.CharField(min_length=2, max_length=2, required=True, widget=forms.TextInput(attrs={"placeholder": "12 (example)", "class": "form-control"}))
    year = forms.CharField(min_length=4, max_length=4, required=True, widget=forms.TextInput(attrs={"placeholder": "2018 (example)", "class": "form-control"}))
    cvv = forms.CharField(min_length=3, max_length=3, required=True,  widget=forms.TextInput(attrs={"placeholder": "cvv card number (123 example)", "class": "form-control"}))
    username = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={"placeholder": "Username", "class": "form-control"}))
    password = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={"placeholder": "Password", "class": "form-control"}))
    verifyPassword = forms.CharField(label="Verifiched Password", required=False, max_length=50, widget=forms.TextInput(attrs={"placeholder": "Verifiched Password","class": "form-control"}))

    def clean_username(self):
        """override del metodo clean_data del campo username, utilizzando la prassi di django, avviene un controllo
        sull'esistenza nel DB della presenza del nome scritto dall'utente, se si viene sollevata l'eccezione sul nome gia esistente"""

        username = self.cleaned_data["username"]
        if (RegisteredClient.objects.filter(username=username).exists()) or (
        HotelKeeper.objects.filter(username=username).exists()):
            raise forms.ValidationError('Username exists')
        else:
            return username

    def clean_verifyPassword(self):
        """override del metodo clean_data del campo verify password, utilizzando la prassi di django, se la password
        è uguale a quella inserita su verify passoword, la password viene criptata e passata per essere
        salvata sul DB, se no viene sollevata eccezione"""
        if self.cleaned_data["verifyPassword"] != self.cleaned_data["password"]:
             raise forms.ValidationError('Verify password wrong')
        passCrypted = pbkdf2_sha256.encrypt(self.cleaned_data["verifyPassword"], rounds=12000, salt_size=32)
        return passCrypted


class CreditCardForm(forms.Form):
    """ classe CreditForm, ogni attributo di questa classe rappresenta un campo di un form
    nel template dove viene mostrato. Questo avviene tramite l'estensione della classe Form
    della libreria django"""

    cardNumber = forms.CharField(min_length=15, max_length=15, required=True, widget=forms.TextInput(attrs={"placeholder": "Your card number", "class": "form-control"}))
    month = forms.CharField(min_length=2, max_length=2, required=True, widget=forms.TextInput(attrs={"placeholder": "12 (example)", "class": "form-control"}))
    year = forms.CharField(min_length=4, max_length=4, required=True, widget=forms.TextInput(attrs={"placeholder": "2018 (example)", "class": "form-control"}))
    cvv = forms.CharField(min_length=3, max_length=3, required=True, widget=forms.TextInput(attrs={"placeholder": "cvv card number (123 example)", "class": "form-control"}))