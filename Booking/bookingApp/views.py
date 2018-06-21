from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from .models import *


contextResultSearch ={}

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
    return render(request, "search.html")

def searchBar(request):
    listResult = []

    if request.method == 'GET':  # quando viene premuto il tasto di ricerca
        searchPatternCity = request.GET.get('search_city', None)
        searchPatternNumber = request.GET.get('search_number', None)
        searchPatternCheckIn = request.GET.get('search_checkin', None)
        searchPatternCheckOut = request.GET.get('search_checkout', None)
        if (searchPatternCity != None and searchPatternNumber != None and\
            searchPatternCheckIn != None and searchPatternCheckOut != None):

            for r in Room.objects.all():
                if (r.hotelId.address.returnCity() == searchPatternCity and \
                        r.hotelId.address.returnCity() == searchPatternNumber):
                    for b in Booking.objects.all():
                        if (r not in Booking.objects.all() or\
                              (b.checkIn < searchPatternCheckIn and b.checkOut > searchPatternCheckOut)):
                            listResult.append(r.hotelId.name, r.roomNumber, IncludedService.objects.filter(r))
    else:
        return redirect("/search/")


    context = {'listResult': listResult}  # è  buona norma passare context a render

    return render(request, "search.html", context)

"prenotazione: " \
"controllo se non vi è utente loggato" \
"primo ramo" \
"form simil a iscrizione (- pass e usern) e scelta registazione e salvataggio" \
"e dettagli camera" \
"secondo ramo" \
"visualizzione dettagli prenotazione e ricerca utente per creare una Prenotazione"
def bookARoom(request):
    if(request.session == 'null'):
        if(request.method == 'POST'):
            formBooking = PaymentForm(request.POST)
            if (formBooking.is_valid()):
                name = formBooking.cleaned_data['name']
                surname = formBooking.cleaned_data['surname']
                birthday = formBooking.cleaned_data['birthday']
                cf = formBooking.cleaned_data['cf']
                email = formBooking.cleaned_data['email']
                street =  formBooking.cleaned_data['street']
                civicNumber = formBooking.cleaned_data['street']
                city = formBooking.cleaned_data['street']
                zipCode = formBooking.cleaned_data['street']
                cardNumber = formBooking.cleaned_data['cardNumber']
                month = formBooking.cleaned_data['month']
                year = formBooking.cleaned_data['year']
                cvv = formBooking.cleaned_data['cvv'] ##
                checkIn = formBooking.cleaned_data['checkin']
                checkOut = formBooking.cleaned_data['checkout']
                room = formBooking.cleaned_data['room']
                checkNewUser = formBooking.checkNewUser.cleaned_data['checkNewUser']

                if int(month)<0 or int(month)>12 or int(year < 2018 or (int(month) < 6 and int(year) <= 2018)):
                    return redirect('booking/')

                card = CreditCard (cardNumber, year, month, cvv)
                card.save()
                address = Address (street, civicNumber, city, zipCode)
                address.save()
                user = User (name, surname, birthday, cf, email, address, card)
                user.save()
                booking = Booking (user, room, checkIn, checkOut)
                booking.save()

                context = {'paymentForm': formBooking}
                return render(request, 'booking/', context)
    else:
        userName = request.session['usr']
        for userAtrs in RegisteredUser.objects.all():
            if (userAtrs.userName == userName):
                userSession = userAtrs
                break
        if (request.method == 'POST'):
            formBooking = PaymentForm(request.POST)

            checkIn = formBooking.cleaned_data['checkin']
            checkOut = formBooking.cleaned_data['checkout']
            room = formBooking.cleaned_data['room']

            booking = Booking(userSession, room, checkIn, checkOut)
            booking.save()

            context = {'paymentForm': formBooking}
            return render(request, 'booking/', context)

def hotelsList(request):
    hotelKeeperUsr = request.session["usr"]
    listHt = []
    cont = 0

    for ht in Hotel.objects.all():
        if (hotelKeeperUsr == ht.hotelKeeperId.userName):
            for room in Room.objects.all():
                if (room.hotelId.address == ht.address):
                    cont+=1
            listHt.append((ht, cont))

    context = {'hotelList': listHt}
    return render(request, 'viewListOfHotels.html', context)

def hotelDetail(request):
    listaCamereHotel = []

    hotelName = request.GET.get('name',None)
    hotelNumber = request.GET.get('civN',None)
    hotelCity = request.GET.get('city',None)

    for ht in Hotel.objects.all():
        if(ht.name == hotelName and ht.address.houseNumber == int(hotelNumber) and ht.address.city == hotelCity):
            print("qua arrivo")
            for rm in Room.objects.all():
                if(rm.hotelId == ht):
                    listaCamereHotel.append(rm)

            context = {'hotel': ht,'roomList': listaCamereHotel}

    return render(request,"manageHotel.html",context)


def bookARoom(request):
    pass
