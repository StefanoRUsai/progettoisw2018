from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
from .models import *
import datetime
from django.contrib import auth

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
    if 'usr' in request.session:
        if 'usrType' in request.session and request.session['usrType'] == 'regUser':
            return redirect('/homeRegistered/')
        else:
            return redirect('/home/')
    else:
        if(request.method == 'POST'):
            form = formLogin(request.POST)
            if(form.is_valid()):
                #Setto in sessione le variabili relative all'utente loggato tranne la password
                userN = form.cleaned_data['username']
                passW = form.cleaned_data['password']

                for ut in RegisteredUser.objects.all():
                    if(ut.userName == userN and ut.password == passW):
                        request.session['usr'] = form.cleaned_data['username']
                        request.session['usrType'] = 'regUser'
                        return redirect('/homeRegistered/')
                for ut in HotelKeeper.objects.all():
                    if (ut.userName == userN and ut.password == passW):
                        request.session['usr'] = form.cleaned_data['username']
                        request.session['usrType'] = 'hotelKeeper'
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
    listPr = []

    try:
        hotelKeeperUsr = request.session["usr"]
    except:
        hotelKeeperUsr = None

    if hotelKeeperUsr != None:

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

            context = {'form': form}
            return render(request,"addRoom.html",context)
    else:
        form = AddRoomForm()

    context = {'formAddRoom': form}
    return render(request, 'addRoom.html', context)


def isFreeUsername(toBeChecked):
    flag = True
    for ut in RegisteredUser.objects.all():
        if(ut.userName == toBeChecked):
            flag =  False
    for ut in HotelKeeper.objects.all():
        if(ut.userName == toBeChecked):
            flag =  False
    return flag


def registerUser(request):
    if 'usr' in request.session:
        if 'usrType' in request.session and request.session['usrType'] == 'regUser':
            return redirect('/homeRegistered/')
        else:
            return redirect('/home/')
    else:
        if (request.method == 'POST'):
            form = RegistrationForm(request.POST)
            if (form.is_valid() and isFreeUsername(str(form.cleaned_data['userName'])) and
                    form.cleaned_data['password'] == form.cleaned_data['verifyPassword']):
                # Setto in sessione le variabili relative all'utente loggato tranne la password
                name = form.cleaned_data['name']
                surname = form.cleaned_data['surname']
                bd = form.cleaned_data['birthday']
                codF = form.cleaned_data['cf']
                emailAddr = form.cleaned_data['email']
                street = form.cleaned_data['street']
                civicNr = form.cleaned_data['civicNumber']
                userCity = form.cleaned_data['city']
                cap = form.cleaned_data['zipCode']
                userN = form.cleaned_data['userName']
                passW = form.cleaned_data['password']

                hotelKeeper = form.cleaned_data['hotelKeeper']

            # creo prima l'oggetto di tipo indirizzo
            userAddr = Address(street=str(street), houseNumber=str(civicNr), city=str(userCity), zipCode=str(cap))
            userAddr.save()

            # creo poi l'oggetto ut di tipo RegisteredUser che comprende l'oggetto userAddr creato poco sopra
            if (hotelKeeper != True):
                ut = RegisteredUser(name=str(name), surname=str(surname),
                                    birthday=str(bd), cf=str(codF),
                                    email=str(emailAddr), userName=str(userN),

                                    password=str(passW), address=userAddr)
                ut.save()
            else:
                hk = HotelKeeper(name=str(name), surname=str(surname),
                                 birthday=str(bd), cf=str(codF),
                                 email=str(emailAddr), userName=str(userN),

                                 password=str(passW), address=userAddr)
                hk.save()

            request.session['usr'] = userN

            if hotelKeeper != True:
                return redirect('/homeRegisteredUser/')
            else:
                return redirect('/home/')

        else:  # Qui ci si entra in caso di prima di prima visualizzazione o richiesta GET
            form = RegistrationForm()

    context = {'form' : form}
    return render(request,'signUp.html',context)



def viewProfileUser(request):
    userName = request.session['usr']
    for userAtrs in RegisteredUser.objects.all():
        if(userAtrs.userName==userName):
            userSession = userAtrs
            break

    flag = False

    creditCardOfUser = None
    for creditCard in CreditCard.objects.all():
        if (userSession.id == creditCard.owner.id):
            creditCardOfUser = creditCard
            flag=True
            break


    context = {'userProfile': userAtrs, 'creditCardView': creditCardOfUser, 'flag':flag}
    return render(request, 'profile.html', context)


def searchResults(request):
    listResult = []

    if request.method == 'GET':  # quando viene premuto il tasto di ricerca
        searchPatternCity = request.GET.get('search_city', None)
        searchPatternNumber = request.GET.get('search_number', None)
        searchPatternCheckIn = request.GET.get('search_checkin', None)
        searchPatternCheckOut = request.GET.get('search_checkout', None)

        if (searchPatternCity != None and searchPatternNumber != None and \
                searchPatternCheckIn != None and searchPatternCheckOut != None):

            for r in Room.objects.all():
                if (r.hotelId.address.city == searchPatternCity and\
                        str(r.capacity) == searchPatternNumber):
                     for b in Booking.objects.all():
                        if (r.id not in Booking.objects.filter()):
                            listIn = searchPatternCheckIn.split("-")
                            listOut = searchPatternCheckOut.split("-")
                            logIn_dt = datetime.datetime(int(listIn[0]), int(listIn[1]), int(listIn[2]))
                            logOut_dt = datetime.datetime(int(listOut[0]), int(listOut[1]), int(listOut[2]))
                            request.session['logIn_dt'] = searchPatternCheckIn
                            request.session['logOut_dt'] = searchPatternCheckOut
                            between = Booking.objects.filter(checkIn=logIn_dt, checkOut=logOut_dt)
                            if between.exists():
                                return render(request, "search.html")
                            else:
                                tmp = [r.hotelId.name, r.roomNumber, r.price, "DEFAULT", r.hotelId.photoUrl, r.id]
                                listResult.append(tmp)

    if len(listResult) > 0:
        context = {'listResult': listResult}  # è  buona norma passare context a render
    else:
        context = {'listaVuota': '1'}

    return render(request, "search.html", context)



def searchBar(request):
    return render(request, "searchBar.html")

def verificationTypeUser(request):
    """<Booking a Room>
    Verifica della tipologia di utente:"""
    try:
        userName = request.session['usr']
    except:
        userName = None
    if userName != None:
        for user in RegisteredUser.objects.all():
            if (user.userName == userName):
                return user
    return None


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
    hotel = None

    hotelName = request.GET.get('name',None)
    hotelNumber = request.GET.get('civN',None)
    hotelCity = request.GET.get('city',None)

    for ht in Hotel.objects.all():
        if(ht.name == hotelName and ht.address.houseNumber == int(hotelNumber) and ht.address.city == hotelCity):
            print("qua arrivo")
            hotel = ht
            for rm in Room.objects.all():
                if(rm.hotelId == hotel):
                    listaCamereHotel.append(rm)

    if(hotel != None):
        context = {'hotel': hotel,'roomList': listaCamereHotel}
    else:
        return HttpResponse("<h3>Nessun dettaglio al momento disponibile</h3>")


    return render(request,"manageHotel.html",context)

""" check su bookin not registered ora funziona"""
def bookingNotRegistered(request, roomBoking):

    if (request.method == 'POST'):
        formBooking = PaymentForm(request.POST)
        if (formBooking.is_valid()):
            name = formBooking.cleaned_data['name']
            surname = formBooking.cleaned_data['surname']
            bd = formBooking.cleaned_data['birthday']
            codF = formBooking.cleaned_data['cf']
            emailAddr = formBooking.cleaned_data['email']
            street = formBooking.cleaned_data['street']
            civicNr = formBooking.cleaned_data['civicNumber']
            userCity = formBooking.cleaned_data['city']
            cap = formBooking.cleaned_data['zipCode']
            cardNumber = formBooking.cleaned_data['cardNumber']
            month = formBooking.cleaned_data['month']
            year = formBooking.cleaned_data['year']
            cvv = formBooking.cleaned_data['cvv']
            #if int(month) < 0 or int(month) > 12 or int(year < 2018 or (int(month) < 6 and int(year) <= 2018)):
            print('arrivo qui carta? ')
            userAddr = Address(street=str(street), houseNumber=str(civicNr), city=str(userCity), zipCode=str(cap))
            userAddr.save()
            ut = User(name=str(name), surname=str(surname), birthday=bd, cf=str(codF),
                                email=str(emailAddr), address=userAddr)
            print('arrivo qui persona?')
            ut.save()

            card = CreditCard(owner=ut, cardNumber=cardNumber, expirationYear=year,
                              expirationMonth=month, cvvCode = cvv)
            card.save()

            try:
                searchPatternCheckIn = request.session['logIn_dt']
                searchPatternCheckOut = request.session['logOut_dt']
                listIn = searchPatternCheckIn.split("-")
                listOut = searchPatternCheckOut.split("-")
                logIn_dt = datetime.datetime(int(listIn[0]), int(listIn[1]), int(listIn[2]))
                logOut_dt = datetime.datetime(int(listOut[0]), int(listOut[1]), int(listOut[2]))
                booking = Booking(customerId=ut, roomId=roomBoking, checkIn=logIn_dt, checkOut=logOut_dt)
                booking.save()
            except:
                booking = None



            return redirect('/booking/')

    else:
        formBooking = PaymentForm()

    return formBooking


def bookingRegisteredUserWithoutCard(request, user, roomBooking):
    if (request.method == 'POST'):
        formBooking = creditCard(request.POST)
        if (formBooking.is_valid()):
            cardNumber = formBooking.cleaned_data['cardNumber']
            month = formBooking.cleaned_data['month']
            year = formBooking.cleaned_data['year']
            cvv = formBooking.cleaned_data['cvv']
            card = CreditCard(owner=user, cardNumber=cardNumber, expirationYear=year,
                              expirationMonth=month, cvvCode=cvv)
            card.save()


            try:
                searchPatternCheckIn = request.session['logIn_dt']
                searchPatternCheckOut = request.session['logOut_dt']
                listIn = searchPatternCheckIn.split("-")
                listOut = searchPatternCheckOut.split("-")
                logIn_dt = datetime.datetime(int(listIn[0]), int(listIn[1]), int(listIn[2]))
                logOut_dt = datetime.datetime(int(listOut[0]), int(listOut[1]), int(listOut[2]))
                booking = Booking(customerId=user, roomId=roomBooking, checkIn=logIn_dt, checkOut=logOut_dt)
                booking.save()
            except:
                booking = None

            return redirect('/booking/')
    else:
        formBooking = creditCard()

    return formBooking




def bookARoom(request):

    try:
        roomid = request.GET.get('roomid', None)
    except:
        roomid = None

    username = verificationTypeUser(request)

    roomBooking = Room.objects.get(id=roomid)

    flagRegistered = False
    flagNotRegistered = False
    flagRegisteredWithoutCard =False
    try:
        user = RegisteredUser.objects.get(userName = str(username))
    except ObjectDoesNotExist:
        user = None

    if user == None:
        formBooking = bookingNotRegistered(request, roomBooking)
        flagNotRegistered =True
    else:
        try:
            creditCardUser = CreditCard.objects.get(owner=user.id)
        except ObjectDoesNotExist:
            creditCardUser = None

        if creditCardUser == None:
            formBooking = bookingRegisteredUserWithoutCard(request, user, roomBooking)
            flagRegisteredWithoutCard = True
        else:
            flagRegistered = True
            try:
                searchPatternCheckIn = request.session['logIn_dt']
                searchPatternCheckOut = request.session['logOut_dt']
                listIn = searchPatternCheckIn.split("-")
                listOut = searchPatternCheckOut.split("-")
                logIn_dt = datetime.datetime(int(listIn[0]), int(listIn[1]), int(listIn[2]))
                logOut_dt = datetime.datetime(int(listOut[0]), int(listOut[1]), int(listOut[2]))
                booking = Booking(customerId=user, roomId=roomBooking, checkIn=logIn_dt, checkOut=logOut_dt)
                booking.save()
            except:
                booking = None

    if flagNotRegistered == True:
        context = {'roomBooking' : roomBooking, 'formBooking': formBooking}
    if flagRegisteredWithoutCard == True:
        context = {'roomBooking' : roomBooking, 'formBookingwithout': formBooking, 'bookingUser': user }
    if flagRegistered == True:
        context = {'roomBooking' : roomBooking, 'bookingUser': user, 'creditCardUser': creditCardUser}

    return render(request, 'payment_form.html', context)



def logout_view(request):
    if 'usr' in request.session:
        del request.session['usr']

        if 'usrType' in request.session:
            del request.session['usrType']
    else:
        print('no usr in sessione')

    return redirect("/")
