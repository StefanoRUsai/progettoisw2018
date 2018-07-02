from django.shortcuts import render, redirect, render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from .forms import *
from .models import *
import datetime
from passlib.hash import pbkdf2_sha256
from django.contrib import auth



def notRegisteredHome(request):
    """ funzione per il controllo della view della home di un utente/cliente non registrato, qui vengono mostrate delle possibili
    camere libere"""

    #variabile di appoggio per non ciclare su tutti gli hotel sul database
    contatore = 0
    #variabile per la lista da passare come contesto per la view, cioè i dati che verranno tenuti nella sessione
    lista = []

    #se esiste un utente nella sessione verrà reindirizzato
    if 'usr' in request.session:
        if 'usrType' in request.session and request.session['usrType'] == 'regUser':
            # se l'utente è un cliente registrato verrà indirizzato alla sua home
            return redirect('/homeRegistered/')
        else:
            # se l'utente è un albergatore verrà indirizzato alla sua home
            return redirect('/home/')

    #estrazione dalla tabella hotel dei primi 3 oggetti nella tabella
    for ht in Hotel.objects.all():
        if(contatore < 3):
            lista.append(ht)
            contatore = contatore + 1


    if(len(lista) >= 3):
        #nel contesto si passano 3 oggetti di tipo hotel se sono esistenti
        context = {'hotel1': lista[0], 'hotel2': lista[1], 'hotel3': lista[2]}
    elif(len(lista) == 2):
        # nel contesto si passa un dizionario con 3 oggetti di tipo hotel, di cui 2 uguali, se esistono almeno 2 oggetti distinti
        context = {'hotel1': lista[0], 'hotel2': lista[1], 'hotel3': lista[0]}
    else:
        #nel contesto si restituisce un messaggio dove viene riportato che non ci sono abbastanza hotel nel DB
        context = {"message": "Two hotels are the minimum required"}
        return render_to_response("messages.html",context)


    return render(request,'homeNotRegisteredClient.html', context)


def login(request):
    """ funzione per il controllo della view di login, qui viene mostrato il form del login"""

    #condizione per vedere la variabile 'usr' esiste nella sessione
    if 'usr' in request.session:
        #condizione che controlla il tipo utente loggato
        if 'usrType' in request.session and request.session['usrType'] == 'regUser':
            #se l'utente è un cliente registrato viene reindirizzato alla home dell'utente registrato
            return redirect('/homeRegistered/')
        else:
            #se è un HotelKeeper viene indirizzato alla sua home
            return redirect('/home/')

    #richiamo del form se il metodo è di tipo POST
    if(request.method == 'POST'):
        #assegnamento alla variabile form, il form LoginForm con i dati che verra passata come context
        form = LoginForm(request.POST)
        #se il form viene valutato valido, non son state sollevate eccezioni e i campi compilati in maniera corretta
        if(form.is_valid()):
            #dal form di login si recupera il campo username e viene assegnato alla variabile username
            username = form.cleaned_data['username']

            #se l'username è presente sulla tabella dei clienti registrati viene restituito true tramite un query sul DB
            if(RegisteredClient.objects.filter(username=username).exists()):
                #viene settato in sessione l'username del cliente
                request.session['usr'] = form.cleaned_data['username']
                #viene settato il tipo di account
                request.session['usrType'] = 'regUser'
                #viene reindirizzato alla home dei clienti registrati
                return redirect('/homeRegistered/')

            #se l'username è presente sulla tabella dell'albergatore viene restituito true tramite un query sul DB
            if (HotelKeeper.objects.filter(username=username).exists()):
                # viene settato in sessione l'username dell'albergatore
                request.session['usr'] = form.cleaned_data['username']
                # viene settato il tipo di account
                request.session['usrType'] = 'hotelKeeper'
                # viene reindirizzato alla home dei clienti registrati
                return redirect('/home/')

    else:
        #se  si entra per la prima volta sul template la variabile form non conterrà nulla
        form = LoginForm()

    #si assegna al context un dizionario chiave valore, dove il valore è il form
    context = {'form' : form}

    return render(request,'login.html', context)


def registeredClientHome(request):
    """ funzione per il controllo della view della home di un utente/cliente registrato, qui vengono mostrate delle possibili
    camere libere"""

    #variabile di appoggio per non ciclare su tutti gli hotel sul database
    contatore = 0
    #variabile per la lista da passare come contesto per la view, cioè i dati che verranno tenuti nella sessione
    lista = []

    if 'usr' in request.session:
        #se l'utente in sessione è di tipo albergatore e cerca di accedere a questa pagina, viene reindirizzato sulla sua home
        if 'usrType' in request.session and request.session['usrType'] == 'hotelKeeper':
            return redirect('/home/')
    else:
        #se non esiste non c'è niente in sessione viene reindirizzato sulla sua home apposita
        return redirect('//')

    #estrazione dalla tabella hotel dei primi 3 oggetti nella tabella
    for ht in Hotel.objects.all():
        if(contatore < 3):
            lista.append(ht)
            contatore = contatore + 1

    if(len(lista) >= 3):
        #nel contesto si passano 3 oggetti di tipo hotel se sono esistenti
        context = {'hotel1': lista[0], 'hotel2': lista[1], 'hotel3': lista[2]}
    elif(len(lista) == 2):
        # nel contesto si passa un dizionario con 3 oggetti di tipo hotel, di cui 2 uguali, se esistono almeno 2 oggetti distinti
        context = {'hotel1': lista[0], 'hotel2': lista[1], 'hotel3': lista[0]}
    else:
        #nel contesto si restituisce un messaggio dove viene riportato che non ci sono abbastanza hotel nel DB
        context = {"message": "Two hotels are the minimum required"}
        return render_to_response("messages.html",context)

    return render(request, 'homeRegisteredClient.html', context)


def hotelKeeperHome(request):
    """ funzione per il controllo della view della home di un albergatore, qui vengono mostrate le prenotazioni
    come richiesto dal progetto"""
    listBooking = []

    if 'usr' in request.session:
        # se l'utente in sessione è di tipo cliente registrato, viene indirizzato sulla sua home
        if 'usrType' in request.session and request.session['usrType'] == 'regUser':
            return redirect('/homeRegistered/')
    else:
        #se non esiste non c'è niente in sessione viene reindirizzato sulla sua home apposita
        return redirect('//')

    #si assegna l'username alla variabile hotelKeeperUsr
    hotelKeeperUsr = request.session["usr"]

    #si controlla sulla tabella Booking se ci sono prenotazioni per questo Albergatore
    for b in Booking.objects.all():
        if (hotelKeeperUsr == b.roomId.hotelId.hotelKeeperId.username):
            if b not in listBooking:
                #si aggiunge alla lista ogni prenotazione associata a un hotel dell'albergatore loggato
                listBooking.append(b)

    #si passa nel contesto un dizionario con i dati riguardanti le prenotazioni
    context = {'listaPrenotazioni': listBooking}
    return render(request, 'homeHotelKeeper.html', context)


def addHotel (request):
    """ funzione per il controllo della view per aggiungere degli hotel, tramite un form,  alla lista di un albergatore"""

    # richiamo del form se il metodo è di tipo POST
    if request.method == 'POST':
        #assegnamento alla variabile form, il form AddHotelForm con i dati che verra passata come context
        form = AddHotelForm(request.POST)
        if(form.is_valid()):

            nameR = form.cleaned_data['name']
            descriptionR = form.cleaned_data['description']
            streetR = form.cleaned_data['street']
            houseNumberR = form.cleaned_data['houseNumber']
            cityR = str(form.cleaned_data['city']).lower()
            zipCodeR = form.cleaned_data['zipCode']
            photoUrlR = "static/img/" + str(form.cleaned_data['photoUrl'])

            #creazione di un di un oggetto di tipo indirizzo
            adress = Address(street=str(streetR), houseNumber=int(houseNumberR), city=str(cityR), zipCode=str(zipCodeR))

            #controllo sulla tabella hotel se esistono gia hotel a quell'indirizzo, se sì. Si restituisce un messaggio di errore
            for ht in Hotel.objects.all():
                if(ht.address.city == adress.city and ht.address.street == adress.street and ht.address.houseNumber == adress.houseNumber):
                    context = {"message" : "An hotel is already present at this address"}
                    return render_to_response('messages.html',context)

            #controllo sulla tabella dei clienti registrati registeredclient se esiste quell'indirizzo
            for r in RegisteredClient.objects.all():
                if (r.address.city == adress.city and r.address.street == adress.street and r.address.houseNumber == adress.houseNumber):
                    context = {"message": "A user of Booking.isw lives at this address"}
                    return render_to_response('messages.html', context)

            #controllo sulla tabella degli albergatori se esiste quell'indirizzo
            for r in HotelKeeper.objects.all():
                if (r.address.city == adress.city and r.address.street == adress.street and r.address.houseNumber == adress.houseNumber):
                    context = {"message": "An hotel keeper of Booking.ISW lives at this address"}
                    return render_to_response('messages.html', context)

            adress.save()

            username = request.session['usr']

            #si controlla che l'username sia nella lista degli albergatori
            for hk in HotelKeeper.objects.all():
                if(hk.username == str(username)):
                    # hotelKeeper Foreign Key
                    htFK = hk
                    #si crea l'hotel e si aggiunge al database
                    hotel = Hotel(name=str(nameR),description=str(descriptionR),hotelKeeperId=htFK,address=adress,photoUrl=str(photoUrlR))
                    hotel.save()
                    break

            return redirect('/hotels/')
    else:
        form = AddHotelForm()
    context = {"form" : form}
    return render(request, 'addHotel.html',context)


def addRoomToHotel(request):
    """ funzione per il controllo della view per aggiungere delle stanze agli hotel,
        tramite un form"""

    if request.method == 'POST':
        form = AddRoomForm(request.POST)
        if(form.is_valid()):
            #liste di supporto
            roomListWhereAdd = []
            servicesListToAdd = []

            #recupero dei dati dalla sessione
            hotelWhereAddName = request.session['htName']
            hotelWhereAddCivN = request.session['htCivN']

            #recupero dei dati dal form vengono assegnati alle variabili
            roomNumber = form.cleaned_data['roomNumber']
            bedsNumber = form.cleaned_data['bedsNumber']
            services = form.cleaned_data['services']
            priceR = float(form.cleaned_data['price'])

            #controllo sul prezzo, numero di stanza e capacità
            if(priceR > 0.0 and int(roomNumber) > 0 and int(bedsNumber) > 0):
                for ht in Hotel.objects.all():
                    #se sono soddisfatti si ottiene l'oggetto hotel
                    if(ht.name == str(hotelWhereAddName) and ht.address.houseNumber == int(hotelWhereAddCivN)):
                        hotelWhereAdd = ht
                        break
                #si cicla sulla tabelle delle stanze, quando la stanza appartiene all'hotel viene aggiunta alla lista di supporto
                for rm in Room.objects.all():
                    if (rm.hotelId == hotelWhereAdd):
                        roomListWhereAdd.append(rm)

                #se la lista è di lunghezza 0 si crea la stanza e si aggiunge al databse
                if (len(roomListWhereAdd) == 0):
                    tmpRoom = Room(roomNumber=int(roomNumber), capacity=int(bedsNumber), price=priceR, hotelId=hotelWhereAdd)
                    tmpRoom.save()
                else:
                    #se la lista ha una dimensione diversa da 0 si cicla su di essa e si controlla se esiste gia una stanza con quel numero
                    for r in roomListWhereAdd:
                        if (r.roomNumber == int(roomNumber)):
                            context = {"message": "Room number already exist in the structure " + str(hotelWhereAdd.name)}
                            return render_to_response("messages.html", context)

                    # aggiungere il servizio sennò l'oggetto non viene creato
                    tmpRoom = Room(roomNumber=int(roomNumber),capacity=int(bedsNumber),price=priceR,hotelId=hotelWhereAdd)
                    tmpRoom.save()

                    #si inseriscono tutti i servizi alla stanza
                    for s in services:
                        s = IncludedService(service = str(s))
                        s.save()
                        tmpRoom.services.add(s)

                    #eliminazione permanentemente dalla sessione le variabili che non sono più utili
                    del request.session['htName']
                    del request.session['htCivN']

                    return redirect('/hotels/')
    else:
        form = AddRoomForm()
        context = {"form" : form}
        return render(request,'addRoom.html',context)


def isFreeUsername(toBeChecked):
    """funzione di supporto per sapere se un username è libero"""
    flag = True
    #cicla su tutta la tabella dei clienti registrati
    for ut in RegisteredClient.objects.all():
        if(ut.username == toBeChecked):
            flag =  False
    # cicla su tutta la tabella dei clienti registrati
    for ut in HotelKeeper.objects.all():
        if(ut.username == toBeChecked):
            flag =  False

    # registituisce un valore booleano
    return flag


def registerClient(request):
    """ funzione per il controllo della view per registare il cliente,
        tramite un form"""


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

            #si crea l'oggetto indirizzo
            userAddr = Address(street=str(street), houseNumber=str(civicNr), city=str(userCity), zipCode=str(cap))
            userAddr.save()

            #se la variabile booleana hotelKeeper nel form è False viene creato un utente Registrato
            if (hotelKeeper != True):
                ut = RegisteredClient(name=str(name), surname=str(surname),
                                    birthday=str(bd), cf=str(codF),
                                    email=str(emailAddr),address=userAddr,username=str(userN),
                                    password=str(verifyPassword))
                ut.save()
            else:
                #nel caso la variabile sia a True viene creato un albergatore
                hk = HotelKeeper(name=str(name), surname=str(surname),
                                 birthday=str(bd), cf=str(codF),
                                 email=str(emailAddr), username=str(userN),

                                 password=str(verifyPassword), address=userAddr)
                hk.save()
            #viene settato in sessione l'username e il tipo di classe, l'utente una volta registrato viene indirizzato alla propria Home come gia loggato
            request.session['usr'] = userN

            if hotelKeeper != True:
                request.session['usrType'] = 'regUser'
                return redirect('/homeRegistered/')
            else:
                request.session['usrType'] = 'hotelKeeper'
                return redirect('/home/')

    else:
        form = RegistrationForm()

    context = {'form' : form}
    return render(request,'signUp.html',context)


def viewProfileClient(request):
    """ funzione per il controllo dei dati della view profilo dell'utente"""

    #si assegna il nome utente registrato in sessione
    username = request.session['usr']
    #si creano delle variabili di supporto
    userSession = None
    flag_user = True

    #si ottengono i dati dell'utente ciclando sulla tabella  registeredClient
    for userAtrs in RegisteredClient.objects.all():
        if(userAtrs.username==username):
            userSession = userAtrs
            break

    #se  userSession è settato ancora a None si fa la stessa cosa sulla tabella degli Albergatori
    if(userSession==None):
        flag_user = False
        for userAtrs in HotelKeeper.objects.all():
            if (userAtrs.username == username):
                userSession = userAtrs
                break

        #si passano i dati al contesto e si reindirizza alla pagina del profilo dell'albergatore
        context = {'userProfile': userSession,'flag_user': flag_user,}
        return render(request, 'profile.html', context)

    #si controlla se il cliente registrato ha una carta di credito
    flag_card = False
    creditCardOfUser = None
    for creditCard in CreditCard.objects.all():
        if (userSession.id == creditCard.owner.id):
            creditCardOfUser = creditCard
            flag_card = True
            break

    #si crea una variabile di appoggio per le prenotazioni dell'utente
    listBooking = []
    flag_pren = False
    #si crea una lista delle prenotazioni fatte dal cliente
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


    #si passano tutti i dati sull'utente al context e si rindirizza alla sua pagina profilo
    context = {'userProfile': userSession, 'creditCardView': creditCardOfUser, 'listBooking': listBooking, 'flag_user': flag_user,'flag_card':flag_card,'flag_pren':flag_pren}
    return render(request, 'profile.html', context)




def searchResults(request):
    """ funzione per il controllo della view in cui si visualizzaon i dati di ricerca,
        tramite un form,  alla lista di un albergatore"""

    #variabile appoggio per la resituzione
    listResult = []

    #quando viene premuto il tasto di ricerca si passa all'oggetto GET i campi ricercati

    if request.method == 'GET':
        searchPatternCity = request.GET.get('search_city', None)
        searchPatternNumber = request.GET.get('search_number', None)
        searchPatternCheckIn = request.GET.get('search_checkin', None)
        searchPatternCheckOut = request.GET.get('search_checkout', None)

        if (searchPatternCity != None and searchPatternNumber != None and \
                searchPatternCheckIn != None and searchPatternCheckOut != None):

            #si cicla sulla tabelle delle stanze
            for r in Room.objects.all():
                #se la stanza appartiene a un hotel nella citta richiesta e ha quella capacità
                if (r.hotelId.address.city == searchPatternCity and\
                        str(r.capacity) == searchPatternNumber):
                    #si cicla sulla tabella delle prenotazioni
                     for b in Booking.objects.all():
                        if (r.id not in Booking.objects.filter()):
                            #si ottengono la data di checkIn e checkOut in maniera da poterle usare per la ricerca
                            listIn = searchPatternCheckIn.split("-")
                            listOut = searchPatternCheckOut.split("-")
                            #si creano 2 oggetti di tipo datetime per utilizzarli come date
                            logIn_dt = datetime.date(int(listIn[0]), int(listIn[1]), int(listIn[2]))
                            logOut_dt = datetime.date(int(listOut[0]), int(listOut[1]), int(listOut[2]))
                            #si assegnano le date alla sessione per poterle riutilizzare in un secondo momento
                            request.session['logIn_dt'] = searchPatternCheckIn
                            request.session['logOut_dt'] = searchPatternCheckOut
                            #si assegna alla variabile between il risultato di una query filter
                            between = Booking.objects.filter(checkIn=logIn_dt, checkOut=logOut_dt)
                            #si controlla che la data di checkOut sia successiva a quella di checkIn
                            if(logOut_dt < logIn_dt):
                                context = {"message": "Check-out date must be greater than check-in date"}
                                return render_to_response("messages.html", context)
                            #se la data richiesta è occupata si otrna alla search
                            if(between.exists()):
                                return render(request, "search.html")
                            else:
                                #se la data è disponibile si restituisce una lista di stanze disponibili
                                tmp = [r.hotelId.name, r.roomNumber, r.price, r.services, r.hotelId.photoUrl, r.id]
                                if tmp not in listResult:
                                    listResult.append(tmp)

    if len(listResult) > 0:
        context = {'listResult': listResult}
    else:
        context = {'listaVuota': '1'}

    return render(request, "search.html", context)



def searchBar(request):
    """ funzione per il controllo della view searchBar"""
    return render(request, "searchBar.html")



def verificationTypeUser(request):
    """funzione di supporto per la verifica della tipologia di utente:"""
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


def bookARoom(request):
    """funzione per il controllo della view in cui si visualizzaon i dati di ricerca,
    tramite un form,  alla lista di un albergatore"""
    try:
        #si ottiene dall'oggetto GET l'id della stanza che si vuole prenotare
        roomid = request.GET.get('roomid', None)
    except:
        roomid = None

    #si controlla il tipo di utente loggato
    username = verificationTypeUser(request)
    #si ottiene la stanza associata all'id passato dalla ricerca
    roomBooking = Room.objects.get(id=roomid)

    #variabili di supporto
    flagRegistered = False
    flagNotRegistered = False
    flagRegisteredWithoutCard = False


    try:
        #si ottengono i dati che riguardano l'utente loggato
        user = RegisteredClient.objects.get(username=str(username))
    except ObjectDoesNotExist:
        user = None

    #se l'utente non è loggato si utilizza la funzione di supporto e si imposta la flag a True
    if user == None:
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
                username = formBooking.cleaned_data['username']
                passsword = formBooking.cleaned_data['password']
                verifyPassword = formBooking.cleaned_data['verifyPassword']

                # se i campi username, password e verica password son compilati viene registrato un utente
                if (username != '' and passsword != '' and verifyPassword != ''):

                    # creazione dell'oggetto indirizzo
                    userAddress = Address(street=str(street), houseNumber=str(civicNr), city=str(city),
                                          zipCode=str(cap))

                    # salvataggio sul DB dell'oggetto indirizzo
                    userAddress.save()

                    # creazione dell'oggetto registeredClient
                    user = RegisteredClient(name=str(name), surname=str(surname),
                                            birthday=str(bd), cf=str(codF),
                                            email=str(emailAddr), username=str(username),
                                            password=str(verifyPassword), address=userAddress)

                    # salvataggio sul DB dell'oggetto registeredClient
                    user.save()

                    # creazione dell'oggetto registeredClient
                    card = CreditCard(owner=user, cardNumber=cardNumber, expirationYear=year, expirationMonth=month,
                                      cvvCode=cvv)

                    # salvataggio sul DB dell'oggetto carta di credito
                    card.save()

                else:
                    # salvataggio dei dati ai fini della prenotazione nel caso il cliente non voglia registrarsi sul sito

                    userAddress = Address(street=str(street), houseNumber=str(civicNr), city=str(city),
                                          zipCode=str(cap))
                    userAddress.save()

                    user = Client(name=str(name), surname=str(surname), birthday=bd, cf=str(codF), email=str(emailAddr),
                                  address=userAddress)
                    user.save()

                    card = CreditCard(owner=user, cardNumber=cardNumber, expirationYear=year, expirationMonth=month,
                                      cvvCode=cvv)
                    card.save()

                # si richiedono le date dalla sessione
                searchPatternCheckIn = request.session['logIn_dt']
                searchPatternCheckOut = request.session['logOut_dt']
                # si ottengono la data di checkIn e checkOut in maniera da poterle usare per la ricerca
                listIn = searchPatternCheckIn.split("-")
                listOut = searchPatternCheckOut.split("-")
                # si creano 2 oggetti datetime per impostare le date per la prenotazione
                logIn_dt = datetime.datetime(int(listIn[0]), int(listIn[1]), int(listIn[2]))
                logOut_dt = datetime.datetime(int(listOut[0]), int(listOut[1]), int(listOut[2]))
                # creazione oggetto prenotazione
                booking = Booking(customerId=user, roomId=roomBooking, checkIn=logIn_dt, checkOut=logOut_dt)
                # salvataggio prenotazione
                booking.save()
                return redirect('/')

        else:

            formBooking = PaymentForm()
        flagNotRegistered =True
    else:
        #se l'utente esiste si controlla se ha una carta di credito
        try:
            creditCardUser = CreditCard.objects.get(owner=user.id)
        except ObjectDoesNotExist:
            creditCardUser = None
        #se l'utente non ha la carta di credito si utilizza la funzione di supporto per visualizzare il form per crearla
        if creditCardUser == None:
            # richiesta del form
            if (request.method == 'POST'):
                formBooking = CreditCardForm(request.POST)
                if (formBooking.is_valid()):
                    cardNumber = formBooking.cleaned_data['cardNumber']
                    month = formBooking.cleaned_data['month']
                    year = formBooking.cleaned_data['year']
                    cvv = formBooking.cleaned_data['cvv']

                    # creazione dell'oggeto carta di credito
                    card = CreditCard(owner=user, cardNumber=cardNumber, expirationYear=year, expirationMonth=month,
                                      cvvCode=cvv)
                    # salvataggio della carta di credito
                    card.save()

                    # si richiedono le date dalla sessione
                    searchPatternCheckIn = request.session['logIn_dt']
                    searchPatternCheckOut = request.session['logOut_dt']
                    # si ottengono la data di checkIn e checkOut in maniera da poterle usare per la ricerca
                    listIn = searchPatternCheckIn.split("-")
                    listOut = searchPatternCheckOut.split("-")
                    # si creano 2 oggetti datetime per impostare le date per la prenotazione
                    logIn_dt = datetime.datetime(int(listIn[0]), int(listIn[1]), int(listIn[2]))
                    logOut_dt = datetime.datetime(int(listOut[0]), int(listOut[1]), int(listOut[2]))
                    # creazione oggetto prenotazione
                    booking = Booking(customerId=user, roomId=roomBooking, checkIn=logIn_dt, checkOut=logOut_dt)
                    # salvataggio prenotazione
                    booking.save()

                    return redirect('/homeRegistered')

            else:
                formBooking = CreditCardForm()
            flagRegisteredWithoutCard = True
        else:
            #se esiste la carta di credito si registra la prenotazione
            flagRegistered = True
            try:
                #si richiedono le date dalla sessione
                searchPatternCheckIn = request.session['logIn_dt']
                searchPatternCheckOut = request.session['logOut_dt']
                # si ottengono la data di checkIn e checkOut in maniera da poterle usare per la ricerca
                listIn = searchPatternCheckIn.split("-")
                listOut = searchPatternCheckOut.split("-")
                #si creano 2 oggetti datetime per impostare le date per la prenotazione
                logIn_dt = datetime.datetime(int(listIn[0]), int(listIn[1]), int(listIn[2]))
                logOut_dt = datetime.datetime(int(listOut[0]), int(listOut[1]), int(listOut[2]))
                #creazione oggetto prenotazione
                booking = Booking(customerId=user, roomId=roomBooking, checkIn=logIn_dt, checkOut=logOut_dt)
                #salvataggio prenotazione
                booking.save()

                return redirect('/homeRegistered')
            except:
                booking = None

    if flagNotRegistered == True:
        context = {'roomBooking': roomBooking, 'formBooking': formBooking}
    if flagRegisteredWithoutCard == True:
        context = {'roomBooking': roomBooking, 'formBookingwithout': formBooking, 'bookingUser': user }
    if flagRegistered == True:
        context = {'roomBooking': roomBooking, 'bookingUser': user, 'creditCardUser': creditCardUser}

    return render(request, 'payment_form.html', context)


def logoutView(request):
    """controllore view per uscire dalla sessione """
    if 'usr' in request.session:
        del request.session['usr']

        if 'usrType' in request.session:
            del request.session['usrType']


    return redirect("/")