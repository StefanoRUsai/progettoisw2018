from django.shortcuts import render, redirect
from .forms import AddHotelForm,AddRoomForm,formLogin,registrationForm
from .models import *




def notRegisteredHome(request):
    contatore = 0
    lista = []

    for ht in Hotel.objects.all():
        if(contatore < 3):
            lista.append(ht)
            contatore = contatore + 1


    context = { 'hotel1' : lista[0] , 'hotel2' : lista[1] , 'hotel3' : lista[2]}
    return render(request,'homeNotRegisteredUser.html',context)



def login(request):
    if(request.method == 'POST'):
        form = formLogin(request.POST)
        if(form.is_valid()):
            #Setto in sessione le variabili relative all'utente loggato tranne la password
            userN = form.cleaned_data['username']
            passW = form.cleaned_data['password']

            for ut in RegisteredUser.objects.all():
                if(ut.userName == userN and ut.password == passW):
                    request.session['usr'] = form.cleaned_data['username']
                    return redirect('/homeRegistered/')
            for ut in HotelKeeper.objects.all():
                if (ut.userName == userN and ut.password == passW):
                    request.session['usr'] = form.cleaned_data['username']
                    return redirect('/home/')

    else:  #Qui ci si entra in caso di prima di prima visualizzazione o richiesta GET
        form = formLogin()

    context = {'form' : form}
    return render(request,'login.html',context)



def registeredUserHome(request):

    contatore = 0
    lista = []

    for ht in Hotel.objects.all():
        if(contatore < 3):
            lista.append(ht)
            contatore = contatore + 1


    context = { 'hotel1' : lista[0] , 'hotel2' : lista[1] , 'hotel3' : lista[2]}
    return render(request, 'homeRegisteredUser.html', context)

def hotelKeeperHome(request):

    hotelKeeperUsr = request.session["usr"]
    listPr = []
    for pr in Booking.objects.all():

        if (hotelKeeperUsr == pr.roomId.hotelId.hotelKeeperId.userName):
            listPr.append(pr)
    context = {'listaPrenotazioni': listPr}
    return render(request,'homeHotelKeeper.html', context)


def addHotel (request):
    if request.method == 'POST':
        form = AddHotelForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            street = form.cleaned_data['street']
            houseNumber = form.cleaned_data['houseNumber']
            city = form.cleaned_data['city']
            zipCode = form.cleaned_data['zipCode']
            photoUrl = form.cleaned_data['photoUrl']

            adress = Address(street, houseNumber, city, zipCode)

            adress.save()

            hotel = Hotel(name, description, adress, photoUrl)

            hotel.save()

            return redirect('manageHotel')
    else:
        form = AddHotelForm()

    context = {'formAddHotel': form}
    return render(request, 'addHotel.html', context)


def addRoomToHotel(request):
    if request.method == 'POST':
        form = AddRoomForm(request.POST)
        if form.is_valid():
            form.save()

            roomNumber = form.cleaned_data['roomNumber']
            bedsNumber = form.cleaned_data['bedsNumber']

            hotel = Hotel.objects.all().filter(pk=request.getAttribute('hotelId'))

            services = [label for value, label in form.fields['services'].choices if value in form['services'].value()]

            price = form.cleaned_data['price']

            tmpRoom = Room(roomNumber, bedsNumber, price, hotel)
            tmpRoom.save()

            for s in services:
                temp = IncludedService(service=s,room=tmpRoom)
                temp.save()

            return redirect('addRoom')
    else:
        form = AddRoomForm()

    context = {'formAddRoom': form}
    return render(request, 'addRoom.html', context)


def isFreeUsername(toBeChecked):
    for ut in RegisteredUser.objects.all():
        if(ut.username == toBeChecked):
            return False
    return True


def registerUser(request):
    if (request.method == 'POST'):
        form = registrationForm(request.POST)
        if (form.is_valid() and isFreeUsername(str(form.cleaned_data['username']))):
            # Setto in sessione le variabili relative all'utente loggato tranne la password
            name = form.cleaned_data['nome']
            surname = form.cleaned_data['cognome']
            bd = form.cleaned_data['birthday']
            codF = form.cleaned_data['cf']
            emailAddr = form.cleaned_data['email']
            userN = form.cleaned_data['username']
            passW = form.cleaned_data['password']
            rue = form.cleaned_data['street']
            civicNr = form.cleaned_data['civicNumber']
            userCity = form.cleaned_data['city']
            cap = form.cleaned_data['zipCode']

            #creo prima l'oggetto di tipo indirizzo
            userAddr = Address(street=str(rue),houseNumber=str(civicNr),city=str(userCity),zipCode=str(cap))
            Address.save()

            #creo poi l'oggetto ut di tipo RegisteredUser che comprende l'oggetto userAddr creato poco sopra
            ut = RegisteredUser(nome=str(name),cognome=str(surname),birthday=str(bd),cf=str(codF),email=str(emailAddr),username=str(userN),password=str(passW),address=userAddr)
            ut.save()

            request.session['usr'] = userN
            return redirect('/homeRegisteredUser/')

    else:  #Qui ci si entra in caso di prima di prima visualizzazione o richiesta GET
        form = registrationForm()

    context = {'form' : form}
    return render(request,'signUp.html',context)


def viewProfileUser(request):
    userName = request.session['usr']


    for userAtrs in RegisteredUser.objects.all():
        if(userAtrs.userName==userName):
            userSession = userAtrs
            break

    cardCreditNrUserSession = userSession.creditCard.cardNumber

    context={'userProfile':userAtrs, 'creditCardView':cardCreditNrUserSession}
    return render(request, 'profile.html', context)




def searchResults(request):
    pass

def bookARoom(request):
    pass

def hotelsList(request):
    pass

def hotelDetail(request):
    pass
def searchBar(request):
    return render(request,'searchBar.html')