from django.shortcuts import render, redirect, render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from .forms import *
from .models import *
import datetime
from passlib.hash import pbkdf2_sha256
from django.contrib import auth


def notRegisteredHome(request):
    contatore = 0
    lista = []


    if 'usr' in request.session:
        if 'usrType' in request.session and request.session['usrType'] == 'regUser':
            return redirect('/homeRegistered/')
        else:
            return redirect('/home/')


    for ht in Hotel.objects.all():
        if(contatore < 3):
            lista.append(ht)
            contatore = contatore + 1

    if(len(lista) >= 3):
        context = { 'hotel1' : lista[0] , 'hotel2' : lista[1] , 'hotel3' : lista[2]}
    elif(len(lista) == 2):
        context = { 'hotel1' : lista[0] , 'hotel2' : lista[1] , 'hotel3' : lista[0]}
    else:
        context = {"message" : "Two hotels are the minimum required"}
        return render_to_response("messages.html",context)

    return render(request,'homeNotRegisteredClient.html',context)


def login(request):
    if 'usr' in request.session:
        if 'usrType' in request.session and request.session['usrType'] == 'regUser':
            return redirect('/homeRegistered/')
        else:
            return redirect('/home/')

    if(request.method == 'POST'):
        form = LoginForm(request.POST)
        if(form.is_valid()):
            #Setto in sessione le variabili relative all'utente loggato tranne la password
            userN = form.cleaned_data['username']
            passW = form.cleaned_data['password']



            for ut in RegisteredClient.objects.all():
                if(ut.username == userN):
                    request.session['usr'] = form.cleaned_data['username']
                    request.session['usrType'] = 'regUser'
                    return redirect('/homeRegistered/')
            for ut in HotelKeeper.objects.all():
                if (ut.username == userN and pbkdf2_sha256.verify(passW,ut.password)):
                    request.session['usr'] = form.cleaned_data['username']
                    request.session['usrType'] = 'hotelKeeper'
                    return redirect('/home/')

    else:  #Qui ci si entra in caso di prima di prima visualizzazione o richiesta GET
        form = LoginForm()


    context = {'form' : form}
    return render(request,'login.html',context)


def registeredClientHome(request):
    contatore = 0
    lista = []

    if 'usr' in request.session:
        if 'usrType' in request.session and request.session['usrType'] == 'hotelKeeper':
            return redirect('/home/')
    else:
        return redirect('//')

    for ht in Hotel.objects.all():
        if(contatore < 3):
            lista.append(ht)
            contatore = contatore + 1


    if(len(lista) >= 3):
        context = { 'hotel1' : lista[0] , 'hotel2' : lista[1] , 'hotel3' : lista[2]}
    elif(len(lista) == 2):
        context = { 'hotel1' : lista[0] , 'hotel2' : lista[1] , 'hotel3' : lista[0]}
    else:
        context = {"message" : "Two hotels are the minimum required"}
        return render_to_response("messages.html",context)

    return render(request, 'homeRegisteredClient.html', context)


def hotelKeeperHome(request):
    listPr = []

    if 'usr' in request.session:
        if 'usrType' in request.session and request.session['usrType'] == 'regUser':
            return redirect('/homeRegistered/')
    else:
        return redirect('//')

    try:
        hotelKeeperUsr = request.session["usr"]
    except:
        hotelKeeperUsr = None

    if hotelKeeperUsr != None:
        for pr in Booking.objects.all():
            if (hotelKeeperUsr == pr.roomId.hotelId.hotelKeeperId.username):
                listPr.append(pr)

    context = {'listaPrenotazioni': listPr}
    return render(request,'homeHotelKeeper.html', context)


def addHotel (request):
    if request.method == 'POST':
        print("sono in post")
        form = AddHotelForm(request.POST)
        if(form.is_valid()):
            print("è valido")
            nameR = form.cleaned_data['name']
            descriptionR = form.cleaned_data['description']
            streetR = form.cleaned_data['street']
            houseNumberR = form.cleaned_data['houseNumber']
            cityR = str(form.cleaned_data['city']).lower()
            zipCodeR = form.cleaned_data['zipCode']
            photoUrlR = "static/img/" + str(form.cleaned_data['photoUrl'])

            adress = Address(street=str(streetR),houseNumber=int(houseNumberR),city=str(cityR),zipCode=str(zipCodeR))

            for ht in Hotel.objects.all():
                if(ht.address.city == adress.city and ht.address.street == adress.street and ht.address.houseNumber == adress.houseNumber):
                    context = {"message" : "An hotel is already present at this address"}
                    return render_to_response('messages.html',context)

            for r in RegisteredClient.objects.all():
                if (r.address.city == adress.city and r.address.street == adress.street and r.address.houseNumber == adress.houseNumber):
                    context = {"message": "A user of Booking.isw lives at this address"}
                    return render_to_response('messages.html', context)

            for r in HotelKeeper.objects.all():
                if (r.address.city == adress.city and r.address.street == adress.street and r.address.houseNumber == adress.houseNumber):
                    context = {"message": "An hotel keeper of Booking.ISW lives at this address"}
                    return render_to_response('messages.html', context)

            adress.save()

            username = request.session['usr']

            for hk in HotelKeeper.objects.all():
                if(hk.username == str(username)):
                    htFK = hk #hotelKeeper Foreign Key
                    hotel = Hotel(name=str(nameR),description=str(descriptionR),hotelKeeperId=htFK,address=adress,photoUrl=str(photoUrlR))
                    hotel.save()
                    break

            return redirect('/hotels/')
    else:
        form = AddHotelForm()
    context = {"form" : form}
    return render(request, 'addHotel.html',context)


def addRoomToHotel(request):
    if request.method == 'POST':
        form = AddRoomForm(request.POST)
        if(form.is_valid()):
            roomListWhereAdd = []
            servicesListToAdd = []

            #recupero i dati utili da sessione
            hotelWhereAddName = request.session['htName']
            hotelWhereAddCivN = request.session['htCivN']

            #recupero i dati dal form e li salvo nelle variabili
            roomNumber = form.cleaned_data['roomNumber']
            bedsNumber = form.cleaned_data['bedsNumber']
            services = form.cleaned_data['services']
            priceR = float(form.cleaned_data['price'])

            if(priceR > 0.0 and int(roomNumber) > 0 and int(bedsNumber) > 0):
                for ht in Hotel.objects.all():
                    if(ht.name == str(hotelWhereAddName) and ht.address.houseNumber == int(hotelWhereAddCivN)):
                        hotelWhereAdd = ht
                        break

                for rm in Room.objects.all():
                    if (rm.hotelId == hotelWhereAdd):
                        roomListWhereAdd.append(rm)

                if (len(roomListWhereAdd) == 0):
                    tmpRoom = Room(roomNumber=int(roomNumber), capacity=int(bedsNumber), price=priceR, hotelId=hotelWhereAdd)
                    tmpRoom.save()
                else:
                    for r in roomListWhereAdd:
                        if (r.roomNumber == int(roomNumber)):
                            context = {"message": "Room number already exist in the structure " + str(hotelWhereAdd.name)}
                            return render_to_response("messages.html", context)

                    tmpRoom = Room(roomNumber=int(roomNumber),capacity=int(bedsNumber),price=priceR,hotelId=hotelWhereAdd) #aggiungere il servizio sennò l'oggetto non viene creato
                    tmpRoom.save()

                    for s in services:
                        s = IncludedService(service = str(s))
                        s.save()
                        tmpRoom.services.add(s)

                    #elimino permanentemente dalla sessione le variabili che non sono più utili
                    del request.session['htName']
                    del request.session['htCivN']

                    return redirect('/hotels/')
    else:
        form = AddRoomForm()
        context = {"form" : form}
        return render(request,'addRoom.html',context)


def isFreeUsername(toBeChecked):
    flag = True
    for ut in RegisteredClient.objects.all():
        if(ut.username == toBeChecked):
            flag =  False
    for ut in HotelKeeper.objects.all():
        if(ut.username == toBeChecked):
            flag =  False
    return flag


def registerClient(request):
    if 'usr' in request.session:
        if 'usrType' in request.session and request.session['usrType'] == 'regUser':
            return redirect('/homeRegistered/')
        else:
            return redirect('/home/')

    if (request.method == 'POST'):
        form = RegistrationForm(request.POST)
        if (form.is_valid() ):
            # Setto in sessione le variabili relative all'utente loggato tranne la password
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            bd = form.cleaned_data['birthday']
            codF = form.cleaned_data['cf']
            emailAddr = form.cleaned_data['email']
            street = form.cleaned_data['street']
            civicNr = form.cleaned_data['civicNumber']
            userCity = str(form.cleaned_data['city']).lower()
            cap = form.cleaned_data['zipCode']
            userN = form.cleaned_data['username']
            passW = form.cleaned_data['password']
            verifyPassword = form.cleaned_data['verifyPassword']





            hotelKeeper = form.cleaned_data['hotelKeeper']

            # creo prima l'oggetto di tipo indirizzo
            userAddr = Address(street=str(street), houseNumber=str(civicNr), city=str(userCity), zipCode=str(cap))
            userAddr.save()

            # creo poi l'oggetto ut di tipo RegisteredClient che comprende l'oggetto userAddr creato poco sopra
            if (hotelKeeper != True):
                ut = RegisteredClient(name=str(name), surname=str(surname),
                                    birthday=str(bd), cf=str(codF),
                                    email=str(emailAddr),address=userAddr,username=str(userN),
                                    password=str(verifyPassword))
                ut.save()
                #send_mail( 'BOOKING.ISW',"Ciao " + str(ut.name) + "benvenuto su Booking.ISW,se hai ricevuto questa mail significa che la tua registrazione è avvenuta con successo",
                 #                                                'edo.citta@gmail.com',[str(ut.email)],fail_silently=False )
            else:
                hk = HotelKeeper(name=str(name), surname=str(surname),
                                 birthday=str(bd), cf=str(codF),
                                 email=str(emailAddr), username=str(userN),

                                 password=str(verifyPassword), address=userAddr)
                hk.save()

            request.session['usr'] = userN

            if hotelKeeper != True:
                request.session['usrType'] = 'regUser'
                return redirect('/homeRegistered/')
            else:
                request.session['usrType'] = 'hotelKeeper'
                return redirect('/home/')

    else:  # Qui ci si entra in caso di prima di prima visualizzazione o richiesta GET
        form = RegistrationForm()

    context = {'form' : form}
    return render(request,'signUp.html',context)


def viewProfileClient(request):
    username = request.session['usr']
    userSession = None
    flag_user = True

    for userAtrs in RegisteredClient.objects.all():
        if(userAtrs.username==username):
            userSession = userAtrs
            break

    if(userSession==None):
        flag_user = False
        for userAtrs in HotelKeeper.objects.all():
            if (userAtrs.username == username):
                userSession = userAtrs
                break

        context = {'userProfile': userSession,'flag_user': flag_user,}
        return render(request, 'profile.html', context)

    flag_card = False
    creditCardOfUser = None
    for creditCard in CreditCard.objects.all():
        if (userSession.id == creditCard.owner.id):
            creditCardOfUser = creditCard
            flag_card = True
            break

    listBooking = []
    flag_pren = False

    for book in Booking.objects.all():
        if (userSession.id == book.customerId.id):
            for room in Room.objects.all():
                if(room.id==book.roomId.id):
                    for hotel in Hotel.objects.all():
                        if(room.hotelId.id==hotel.id):
                            listBooking.append([book, room, hotel])
                            if (flag_pren==False):
                                flag_pren=True
                            break

    context = {'userProfile': userSession, 'creditCardView': creditCardOfUser, 'listBooking': listBooking, 'flag_user': flag_user,'flag_card':flag_card,'flag_pren':flag_pren}
    return render(request, 'profile.html', context)




def searchResults(request):
    listResult = []

    if request.method == 'GET':  # quando viene premuto il tasto di ricerca
        searchPatternCity = request.GET.get('search_city', None).lower()
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
                            logIn_dt = datetime.date(int(listIn[0]), int(listIn[1]), int(listIn[2]))
                            logOut_dt = datetime.date(int(listOut[0]), int(listOut[1]), int(listOut[2]))
                            request.session['logIn_dt'] = searchPatternCheckIn
                            request.session['logOut_dt'] = searchPatternCheckOut
                            between = Booking.objects.filter(checkIn=logIn_dt, checkOut=logOut_dt)
                            if(logOut_dt < logIn_dt):
                                context = {"message": "Check-out date must be greater than check-in date"}
                                return render_to_response("messages.html", context)
                            if(between.exists()):
                                return render(request, "search.html")
                            else:
                                tmp = [r.hotelId.name, r.roomNumber, r.price, r.services, r.hotelId.photoUrl, r.id]
                                if tmp not in listResult:
                                    listResult.append(tmp)

    if len(listResult) > 0:
        context = {'listResult': listResult}
    else:
        context = {'listaVuota': '1'}

    return render(request, "search.html", context)



def searchBar(request):
    return render(request, "searchBar.html")



def verificationTypeUser(request):
    """<Booking a Room>
    Verifica della tipologia di utente:"""
    try:
        username = request.session['usr']
    except:
        username = None
    if username != None:
        for user in RegisteredClient.objects.all():
            if (user.username == username):
                return user
    return None


def hotelsList(request):
    hotelKeeperUsr = request.session["usr"]
    listHt = []
    cont = 0

    for ht in Hotel.objects.all():
        if (hotelKeeperUsr == ht.hotelKeeperId.username):
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
            hotel = ht
            for rm in Room.objects.all():
                if(rm.hotelId == hotel):
                    listaCamereHotel.append(rm)

    request.session['htName'] = hotel.name
    request.session['htCivN'] = hotel.address.houseNumber

    if(hotel != None):
        context = {'hotel': hotel,'roomList': listaCamereHotel}
    else:
        context = {"message" : "No details to show at the moment"}
        return render_to_response("messages.html",context)


    return render(request,"manageHotel.html",context)



""" check su bookin not registered NON È una view ma una funzione di appoggio"""


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
            city = formBooking.cleaned_data['city']
            cap = formBooking.cleaned_data['zipCode']
            cardNumber = formBooking.cleaned_data['cardNumber']
            month = formBooking.cleaned_data['month']
            year = formBooking.cleaned_data['year']
            cvv = formBooking.cleaned_data['cvv']

            userN = formBooking.cleaned_data['username']
            passW = formBooking.cleaned_data['password']
            verifyPassword = formBooking.cleaned_data['verifyPassword']

            if (userN != None and passW != None and verifyPassword != None):

                userAddr = Address(street=str(street), houseNumber=str(civicNr), city=str(city), zipCode=str(cap))
                userAddr.save()

                ut = RegisteredClient(name=str(name), surname=str(surname),
                                    birthday=str(bd), cf=str(codF),
                                    email=str(emailAddr), username=str(userN),
                                    password=str(verifyPassword), address=userAddr)
                ut.save()

                card = CreditCard(owner=ut, cardNumber=cardNumber, expirationYear=year, expirationMonth=month,
                                  cvvCode=cvv)
                card.save()

            else:
                userAddr = Address(street=str(street), houseNumber=str(civicNr), city=str(city), zipCode=str(cap))
                userAddr.save()

                ut = Client(name=str(name), surname=str(surname), birthday=bd, cf=str(codF), email=str(emailAddr),
                          address=userAddr)
                ut.save()

                card = CreditCard(owner=ut, cardNumber=cardNumber, expirationYear=year, expirationMonth=month,
                                  cvvCode=cvv)
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
            return redirect('/')

    else:
        formBooking = PaymentForm()

    return formBooking

def bookingRegisteredClientWithoutCard(request, user, roomBooking):
    if (request.method == 'POST'):
        formBooking = CreditCardForm(request.POST)
        if (formBooking.is_valid()):
            cardNumber = formBooking.cleaned_data['cardNumber']
            month = formBooking.cleaned_data['month']
            year = formBooking.cleaned_data['year']
            cvv = formBooking.cleaned_data['cvv']

            card = CreditCard(owner=user, cardNumber=cardNumber, expirationYear=year,expirationMonth=month,cvvCode=cvv)
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

            return redirect('/homeRegistered')
    else:
        formBooking = CreditCardForm()

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
    flagRegisteredWithoutCard = False
    try:
        user = RegisteredClient.objects.get(username = str(username))
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
            formBooking = bookingRegisteredClientWithoutCard(request, user, roomBooking)
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

                return redirect('/homeRegistered')
            except:
                booking = None

    if flagNotRegistered == True:
        context = {'roomBooking' : roomBooking, 'formBooking': formBooking}
    if flagRegisteredWithoutCard == True:
        context = {'roomBooking' : roomBooking, 'formBookingwithout': formBooking, 'bookingUser': user }
    if flagRegistered == True:
        context = {'roomBooking' : roomBooking, 'bookingUser': user, 'creditCardUser': creditCardUser}

    return render(request, 'payment_form.html', context)


def logoutView(request):
    if 'usr' in request.session:
        del request.session['usr']

        if 'usrType' in request.session:
            del request.session['usrType']
    else:
        print('no usr in sessione')

    return redirect("/")