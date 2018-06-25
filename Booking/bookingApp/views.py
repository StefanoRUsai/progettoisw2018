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
        return HttpResponse("<h1>Servono almeno due alberghi</h1>")

    return render(request,'homeNotRegisteredUser.html',context)


def login(request):
    if 'usr' in request.session:
        if 'usrType' in request.session and request.session['usrType'] == 'regUser':
            return redirect('/homeRegistered/')
        else:
            return redirect('/home/')

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


    if(len(lista) >= 3):
        context = { 'hotel1' : lista[0] , 'hotel2' : lista[1] , 'hotel3' : lista[2]}
    elif(len(lista) == 2):
        context = { 'hotel1' : lista[0] , 'hotel2' : lista[1] , 'hotel3' : lista[0]}
    else:
        return HttpResponse("<h1>Servono almeno due alberghi</h1>")

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

        nameR = request.POST['name']
        descriptionR = request.POST['description']
        streetR = request.POST['street']
        houseNumberR = request.POST['houseNumber']
        cityR = request.POST['city']
        zipCodeR = request.POST['zipCode']
        photoUrlR = "static/img/" + str(request.POST['photoUrl'])

        adress = Address(street=str(streetR),houseNumber=int(houseNumberR),city=str(cityR),zipCode=str(zipCodeR))
        adress.save()

        for ht in Hotel.objects.all():
            if(ht.address == adress):
                return HttpResponse("<h1>È già presente un hotel a questo indirizzo</h1>")

        for r in RegisteredUser.objects.all():
            if(r.address == adress):
                return HttpResponse("<h1>Vive già qualcuno a questo indirizzo</h1>")

        username = request.session['usr']

        for hk in HotelKeeper.objects.all():
            if(hk.userName == str(username)):
                htFK = hk #hotelKeeper Foreign Key
                hotel = Hotel(name=str(nameR),description=str(descriptionR),hotelKeeperId=htFK,address=adress,photoUrl=str(photoUrlR))
                hotel.save()
                break

        return redirect('/hotels/')
    else:
        form = AddHotelForm()

    return render(request, 'addHotel.html')


def addRoomToHotel(request):
    if request.method == 'POST':
        roomListWhereAdd = []
        servicesListToAdd = []

        #recupero i dati utili da sessione
        hotelWhereAddName = request.session['htName']
        hotelWhereAddCivN = request.session['htCivN']

        #recupero i dati dal form e li salvo nelle variabili
        roomNumber = request.POST['roomNumber']
        bedsNumber = request.POST['bedsNumber']
        services = request.POST.getlist('services')
        priceR = float(request.POST['price'])


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
                    return HttpResponse("<h1>Numero camera già prensente nella struttura " + str(hotelWhereAdd.name) + "</h1>")
            print("anche")
            tmpRoom = Room(roomNumber=int(roomNumber),capacity=int(bedsNumber),price=priceR,hotelId=hotelWhereAdd) #aggiungere il servizio sennò l'oggetto non viene creato
            tmpRoom.save()


        #elimino permanentemente dalla sessione le variabili che non sono più utili
        del request.session['htName']
        del request.session['htCivN']

        return redirect('/hotels/')
    else:
        return render(request, 'addRoom.html')


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
            request.session['usrType'] = 'regUser'
            return redirect('/homeRegistered/')
        else:
            request.session['usrType'] = 'hotelKeeper'
            return redirect('/home/')

    else:  # Qui ci si entra in caso di prima di prima visualizzazione o richiesta GET
        form = RegistrationForm()

    context = {'form' : form}
    return render(request,'signUp.html',context)


def viewProfileUser(request):
    userName = request.session['usr']
    userSession = None
    flag_user = True

    for userAtrs in RegisteredUser.objects.all():
        if(userAtrs.userName==userName):
            userSession = userAtrs
            break

    if(userSession==None):
        flag_user = False
        for userAtrs in HotelKeeper.objects.all():
            if (userAtrs.userName == userName):
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
                                tmp = [r.hotelId.name, r.roomNumber, r.price, r.services, r.hotelId.photoUrl, r.id]
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
            hotel = ht
            for rm in Room.objects.all():
                if(rm.hotelId == hotel):
                    listaCamereHotel.append(rm)

    request.session['htName'] = hotel.name
    request.session['htCivN'] = hotel.address.houseNumber

    if(hotel != None):
        context = {'hotel': hotel,'roomList': listaCamereHotel}
    else:
        return HttpResponse("<h3>Nessun dettaglio al momento disponibile</h3>")


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
            userCity = formBooking.cleaned_data['city']
            cap = formBooking.cleaned_data['zipCode']
            cardNumber = formBooking.cleaned_data['cardNumber']
            month = formBooking.cleaned_data['month']
            year = formBooking.cleaned_data['year']
            cvv = formBooking.cleaned_data['cvv']

            userAddr = Address(street=str(street), houseNumber=str(civicNr), city=str(userCity), zipCode=str(cap))
            userAddr.save()

            ut = User(name=str(name), surname=str(surname), birthday=bd, cf=str(codF),email=str(emailAddr), address=userAddr)
            ut.save()

            card = CreditCard(owner=ut, cardNumber=cardNumber, expirationYear=year,expirationMonth=month, cvvCode = cvv)
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
    flagRegisteredWithoutCard = False
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


def logoutView(request):
    if 'usr' in request.session:
        del request.session['usr']

        if 'usrType' in request.session:
            del request.session['usrType']
    else:
        print('no usr in sessione')

    return redirect("/")