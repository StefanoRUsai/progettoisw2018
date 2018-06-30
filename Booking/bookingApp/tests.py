from django.contrib.sessions.middleware import SessionMiddleware
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client, RequestFactory
import os
import enum
import unittest
import datetime
from .models import *
from .forms import *
from .views import *
from passlib.hash import pbkdf2_sha256


class ModelTest(TestCase):
    def setUp(self):
        addressGlobal = Address(street='via Piave', houseNumber=60, city='Uras', zipCode='78999')
        addressGlobal.save()
        creditCardGlobal = CreditCard(cardNumber=56478397474839375, expirationMonth=12, expirationYear=2020,
                                      cvvCode=666)
        creditCardGlobal.save()
        creditCard = CreditCard(cardNumber=788888999987900, expirationMonth=10, expirationYear=2019, cvvCode=555)
        creditCard.save()
        person = Person(name='Stefano', surname='Marcello', email='smarcello@gmail.com',
                        birthday=datetime.date(1987, 10, 11), cf='MRCSTN84S13A355X', address=addressGlobal)
        person.save()
        hotelKeeper = HotelKeeper(name='Giorgia', surname='Congiu', email='giogio.com',
                                  birthday=datetime.date(1996, 10, 20), cf='CNGGRG96R60A355U', username='giogioCong96',
                                  password=str(pbkdf2_sha256.encrypt("isw", rounds=12000,salt_size=32)), address=addressGlobal)
        hotelKeeper.save()
        hotel = Hotel(name='T Hotel', description='Nel cuore di Cagliari...', hotelKeeperId=hotelKeeper,
                      address=addressGlobal)
        hotel.save()
        room1 = Room(capacity=3, price='120.00', hotelId=hotel)
        room1.save()
        service = IncludedService(service=IncludedService.GARAGE, room=room1)
        service.save()
        user = Client(name='Carlo', surname='Puddu', email='cpuddu@gmail.com', birthday=datetime.date(1990, 10, 6),
                    cf='PDDCRL90F06F979T', address=addressGlobal, creditCard=creditCardGlobal)
        user.save()
        registeredUser = RegisteredClient(name='Mario', surname='Cittadini', email='marcit@gmail.com',
                                        birthday=datetime.date(1987, 10, 11), cf='CTTMRA76T607T',
                                        username='marcittttt2018', password='gitPullFailed', address=addressGlobal,
                                        creditCard=creditCardGlobal)
        registeredUser.save()
        booking = Booking(customerId=user, roomId=room1, checkIn=datetime.date(2018, 11, 12),
                          checkOut=datetime.date(2018, 11, 18))
        booking.save()






''' Unitary tests for testing the forms'''
class FormsTest(TestCase):
    def setUp(self):
        addressGlobal = Address(street='via Piave', houseNumber=60, city='Uras', zipCode='78999')
        addressGlobal.save()
        creditCardGlobal = CreditCard(cardNumber=788888999987900, expirationMonth=10, expirationYear=2019, cvvCode=555)
        creditCardGlobal.save()
        r = RegisteredClient(name='Diego', surname='Cittadini', email='marcit@gmail.com',birthday=datetime.date(1987, 10, 11), cf='CTTMRA76T607T',username='diego', password='password', address=addressGlobal,creditCard=creditCardGlobal)
        r.save()


    def tearDown(self):
        pass


    # Tests whether a filled AddHotelForm is valid
    # Expected: a complete form is valid
    def test_AddHotelFormValidity(self):
        # Instantiating an AddHotelForm
        addHotelForm = AddHotelForm()

        # Filling the form
        photo_file = open(os.path.dirname(__file__) + '/../static/img/cortina.jpg', 'rb')
        addHotelForm.name = 'Test hotel'
        addHotelForm.description = 'Hotel used for unitary test'
        addHotelForm.street = 'Test street'
        addHotelForm.houseNumber = 12
        addHotelForm.city = 'Test city'
        addHotelForm.zipCode = '19928'
        addHotelForm.photoUrl = SimpleUploadedFile(photo_file.name, photo_file.read())


        # Testing the form
        self.assertTrue(addHotelForm.is_valid(), addHotelForm.errors)

    # Tests whether a incomplete AddHotelForm is invalid
    # Expected: an incomplete form is not valid
    def test_AddHotelFormIsNotValid(self):
        # Instantiating an AddHotelForm
        addHotelForm = AddHotelForm()

        # Filling the form
        # The form is missing the photoUrl field
        addHotelForm.name = 'Test hotel'
        addHotelForm.description = 'Hotel used for unitary test'
        addHotelForm.street = 'Test street'
        addHotelForm.houseNumber = 12
        addHotelForm.city = 'Test city'
        addHotelForm.zipCode = '19928'

        # Testing the form
        self.assertFalse(addHotelForm.is_valid(), addHotelForm.errors)


    # Tests whether a filled AddRoomForm is valid
    # Expected: a complete form is valid
    def test_AddRoomFormValidity(self):
        # Instantiating an AddRoomForm
        addRoomForm = AddRoomForm()

        # Filling the form
        addRoomForm.roomNumber = 14
        addRoomForm.bedsNumber = 3
        addRoomForm.services = ['GARAGE', 'WIFI']
        addRoomForm.price = 120.0


        # Testing the form
        self.assertTrue(addRoomForm.is_valid(), addRoomForm.errors)


    # Tests whether an incomplete AddRoomForm is invalid
    # Expected: an incomplete form is not valid
    def test_AddRoomFormIsNotValid(self):
        # Instantiating an AddRoomForm
        addRoomForm = AddRoomForm()

        # Filling the form
        # The form is missing the bedsNumber field
        addRoomForm.roomNumber = 14
        addRoomForm.services = ['GARAGE', 'WIFI']
        addRoomForm.price = 120.0

        # Testing the form
        self.assertFalse(addRoomForm.is_valid(), addRoomForm.errors)

    # Tests whether a filled CreditCardForm is valid
    # Expected: a complete form is valid
    def test_CreditCardFormValidity(self):
        # Instantiating a CreditCardForm
        ccForm = CreditCardForm()

        # Filling the form
        ccForm.cardNumber = '1235551223234124'
        ccForm.month = '03'
        ccForm.year = '2019'
        ccForm.cvv = '003'

        # Testing the form
        self.assertTrue(ccForm.is_valid(), ccForm.errors)

    # Tests whether an incomplete CreditCardForm is invalid
    # Expected: an incomplete form is not valid
    def test_CreditCardFormIsNotValid(self):
        # Instantiating a CreditCardForm
        ccForm = CreditCardForm()

        # Filling the form
        # The form is missing the cardNumber field
        ccForm.month = '03'
        ccForm.year = '2019'
        ccForm.cvv = '003'

        # Testing the form
        self.assertFalse(ccForm.is_valid(), ccForm.errors)

    # Tests whether a filled LoginForm is valid
    # Expected: a complete form is valid
    def test_LoginFormValidity(self):
        # Instantiating a LoginForm
        logForm = LoginForm()

        # Filling the form
        logForm.username = 'diego'
        logForm.password = 'password'

        # Testing the form
        self.assertTrue(logForm.is_valid(), logForm.errors)

    # Tests whether an incomplete LoginForm is invalid
    # Expected: an incomplete form is not valid
    def test_LoginFormIsNotValid(self):
        # Instantiating a LoginForm
        logForm = LoginForm()

        # Filling the form
        # The form is missing the username field
        logForm.password = 'password'

        # Testing the form
        self.assertFalse(logForm.is_valid(), logForm.errors)


    # Tests whether a filled RegistrationForm is valid
    # Expected: a complete form is valid
    def test_RegistrationFormValidity(self):
        # Instantiating a RegistrationForm
        regForm = RegistrationForm()

        # Filling the form
        regForm.hotelKeeper = True
        regForm.name = 'Gianni'
        regForm.surname = 'Pinna'
        regForm.birthday = '1990-02-13'
        regForm.cf = 'kjhf240'
        regForm.email = 'sonoGianni@gmail.com'
        regForm.username = 'gianni'
        regForm.password = 'password'
        regForm.verificapassword = 'password'
        regForm.street = 'via torre'
        regForm.civicNumber = 12
        regForm.city = 'torres'
        regForm.zipCode = '42843'

        # Testing the form
        self.assertTrue(regForm.is_valid(), regForm.errors)


    # Tests whether an incomplete RegistrationForm is not valid
    # Expected: an incomplete form is not valid
    def test_RegistrationFormIsNotValid(self):
        # Instantiating a RegistrationForm
        regForm = RegistrationForm()

        # Filling the form
        # The form is missing the email field
        regForm.hotelKeeper = True
        regForm.name = 'Gianni'
        regForm.surname = 'Pinna'
        regForm.birthday = '1990-02-13'
        regForm.cf = 'kjhf240'
        regForm.username = 'gianni'
        regForm.password = 'password'
        regForm.verificapassword = 'password'
        regForm.street = 'via torre'
        regForm.civicNumber = 12
        regForm.city = 'torres'
        regForm.zipCode = '42843'

        # Testing the form
        self.assertFalse(regForm.is_valid(), regForm.errors)



    # Tests whether a filled PaymentForm is valid
    # Expected: a complete form is valid
    def test_PaymentFormValidity(self):
        # Instantiating an AddHotelForm
        payForm = PaymentForm()

        # Filling the form
        payForm.name = 'giovanni'
        payForm.surname = 'frau'
        payForm.birthday = '1992-12-12'
        payForm.cf = 'asff21'
        payForm.email = 'giovanni@gmail.com'
        payForm.street = 'via san giovanni'
        payForm.civicNumber = 12
        payForm.city = 'cagliari'
        payForm.zipCode = '00098'
        payForm.cardNumber = '124124513'
        payForm.month = '05'
        payForm.year = '2001'
        payForm.cvv ='098'
        payForm.username = 'diego'
        payForm.password = 'password'
        payForm.verificapassword = 'password'


        # Testing the form
        self.assertTrue(payForm.is_valid(), payForm.errors)


    # Tests whether a filled PaymentForm is valid
    # Expected: a complete form is valid
    def test_PaymentFormIsNotValid(self):
        # Instantiating an AddHotelForm
        payForm = PaymentForm()

        # Filling the form
        # The form is missing the surname field
        payForm.name = 'giovanni'
        payForm.birthday = '1992-12-12'
        payForm.cf = 'asff21'
        payForm.email = 'giovanni@gmail.com'
        payForm.street = 'via san giovanni'
        payForm.civicNumber = 12
        payForm.city = 'cagliari'
        payForm.zipCode = '00098'
        payForm.cardNumber = '124124513'
        payForm.month = '05'
        payForm.year = '2001'
        payForm.cvv ='098'
        payForm.username = 'diego'
        payForm.password = 'password'
        payForm.verificapassword = 'password'


        # Testing the form
        self.assertFalse(payForm.is_valid(), payForm.errors)








"""User Story 1. hotel keeper registration"""


class RegisteredHotelKeeperTest(TestCase):
    def setUp(self):
        address = Address(street='via lanusei', houseNumber=12, city='Cagliari', zipCode='09127')
        address.save()
        hotelKeeper = HotelKeeper(name='Elena', surname='Puddu', birthday=datetime.date(1980, 1, 1),
                                  cf='pdueln80a21b354a', email='e.puddu@gmail.com', address=address, username='prova23',password=str(pbkdf2_sha256.encrypt("isw", rounds=12000,salt_size=32)))
        address = Address(street='via nuoro', houseNumber=16, city='Cagliari', zipCode='09127')
        address.save()
        registereduser = RegisteredClient(name='Marco', surname='Baldo', birthday=datetime.date(1984, 1, 15),
                                        cf='bldmrc84a15b354a', email='marco.baldo@gmail.com', address=address,
                                        username='baldo', password=pbkdf2_sha256.encrypt("isw", rounds=12000,salt_size=32))
        hotelKeeper.save()
        registereduser.save()

        self.userregistered = registereduser
        self.userhotelkeeper = hotelKeeper
        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def test_RegistrationHotelKeeper(self):
        request = self.request_factory.get('/signUp/', follow=True)
        self.middleware.process_request(request)
        request.session.save()

        form = RegistrationForm(data={'hotelKeeper': True
            , 'name': 'Pinco'
            , 'surname': 'Panco'
            , 'birthday': '2018-10-21'
            , 'cf': '213321321312'
            , 'email': 'baldo@gmail.com'
            , 'username': 'pinco'
            , 'password': 'isw'
            , 'verifyPassword': 'isw'
            , 'street': 'via da qui'
            , 'civicNumber': '666'
            , 'city': 'chenonce'
            , 'zipCode': '02131'})

        self.assertTrue(form.is_valid(), msg=form.errors)

    def test_HomeHotellKeeper(self):
        request = self.request_factory.get('/home/', follow=True)
        self.middleware.process_request(request)
        request.session.save()

        request.session['usr'] = 'prova23'
        request.session['usrType'] = 'hotelKeeper'

        response = hotelKeeperHome(request)

        self.assertEquals(response.status_code, 200)

    def test_HomeHotellKeeperError(self):
        request = self.request_factory.get('/home/', follow=True)
        self.middleware.process_request(request)
        request.session.save()

        request.session['usr'] = 'baldo'
        request.session['usrType'] = 'regUser'

        response = hotelKeeperHome(request)

        self.assertEquals(response.status_code, 302)


"""User story 2. hotel keeper login"""


class LoginHotelKeeperTest(TestCase):
    def setUp(self):
        address = Address(street='via lanusei', houseNumber=12, city='Cagliari', zipCode='09127')
        address.save()
        hotelKeeper = HotelKeeper(name='Elena', surname='Puddu', birthday=datetime.date(1980, 1, 1),
                                  cf='pdueln80a21b354a', email='e.puddu@gmail.com', address=address, username='prova23',
                                  password=str(pbkdf2_sha256.encrypt("isw", rounds=12000,salt_size=32)))
        address = Address(street='via nuoro', houseNumber=16, city='Cagliari', zipCode='09127')
        address.save()
        registereduser = RegisteredClient(name='Marco', surname='Baldo', birthday=datetime.date(1984, 1, 15),
                                        cf='bldmrc84a15b354a', email='marco.baldo@gmail.com', address=address,
                                        username='baldo', password=str(pbkdf2_sha256.encrypt("isw", rounds=12000,salt_size=32)))
        hotelKeeper.save()
        registereduser.save()

        self.userregistered = registereduser
        self.userhotelkeeper = hotelKeeper
        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def test_LoginPageRedirect(self):
        request = self.request_factory.get('/login/', follow=True)
        self.middleware.process_request(request)
        request.session.save()

        request.session['usr'] = self.userhotelkeeper.username
        request.session['usrType'] = 'hotelKeeper'

        response = login(request)

        self.assertEquals(response.status_code, 302)

    def test_LoginHotelKeeper(self):


        form = LoginForm(data={'username': 'prova23',
                               'password': 'isw'})

        self.assertTrue(form.is_valid(), msg=form.errors)

    def test_LoginRegisteredUser(self):
        form = LoginForm(data={'username': self.userregistered.username,
                               'password': self.userregistered.password})

        self.assertTrue(form.is_valid(), msg=form.errors)


'''User story 3. Visualizza lista prenotazioni (hotelKeeperhome)'''


class HotelKeeperHomeTest(TestCase):
    def setUp(self):
        hkAddress = Address(street='via francesco', houseNumber=12, city='savona', zipCode='00989')
        hkAddress.save()
        bookedUser = Client(name='gianni', surname='deGasperi', birthday=datetime.date(1996, 10, 20), cf='fsaf34f32',
                          email='gianni@gmail.com', address=hkAddress)
        bookedUser.save()
        userCreditCard = CreditCard(cardNumber='124563455436', expirationYear='2022', expirationMonth='03',
                                    cvvCode='007', owner=bookedUser)
        userCreditCard.save()
        hotelKeeper = HotelKeeper(name='francesco', surname='fadda', birthday=datetime.date(1996, 10, 20),
                                  cf='dasf12r1324', email='francesco@fadda.net', address=hkAddress,
                                  username='francesco', password=str(pbkdf2_sha256.encrypt("isw", rounds=12000,salt_size=32)))
        hotelKeeper.save()
        hotelAddress = Address(street='via hotel bellissimo', houseNumber=12, city='savona', zipCode='00929')
        hotelAddress.save()
        hotel = Hotel(name='Hotel Acquaragia', description='Hotel bellissimo', hotelKeeperId=hotelKeeper,
                      address=hotelAddress, photoUrl='/static/img/amsterdamHotel.jpg')
        hotel.save()
        bookedRoom = Room(roomNumber=12, capacity=3, price=40.0, hotelId=hotel)
        bookedRoom.save()
        hotelKeeperNoBookings = HotelKeeper(name='filippo', surname='podddesu', birthday=datetime.date(1996, 10, 20),
                                            cf='dasf12r1324', email='filippo@poddesu.net', address=hkAddress,
                                            username='filippo', password=str(pbkdf2_sha256.encrypt("isw", rounds=12000,salt_size=32)) )
        hotelKeeperNoBookings.save()
        booking = Booking(customerId=bookedUser, roomId=bookedRoom, checkIn=datetime.date(2018, 11, 28),
                          checkOut=datetime.date(2018, 11, 20))
        booking.save()

        self.userWithBookings = hotelKeeper
        self.userWithoutBookings = hotelKeeperNoBookings
        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def test_hotelKeeperBookingsVisualization(self):
        request = self.request_factory.get('/home/')
        self.middleware.process_request(request)
        request.session.save()
        request.session['usr'] = self.userWithBookings.username
        request.session['usrType'] = 'hotelKeeper'
        response = hotelKeeperHome(request)
        self.assertContains(response, 'gianni')
        self.assertContains(response, 'Hotel Acquaragia')

    def test_hotelKeeperNoBookingsMessage(self):
        request = self.request_factory.get('/home/')
        self.middleware.process_request(request)
        request.session.save()
        request.session['usr'] = self.userWithoutBookings.username
        request.session['usrType'] = 'hotelKeeper'
        response = hotelKeeperHome(request)
        self.assertContains(response, "You have not reservations in your hotels!")


''''User story 4. (req. ViewHotelList)'''


class HotelsListTest(TestCase):
    def setUp(self):
        hkAddress = Address(street='via francesco', houseNumber=12, city='savona', zipCode='00989')
        hkAddress.save()
        hotelKeeper = HotelKeeper(name='francesco', surname='fadda', birthday=datetime.date(1996, 10, 20),
                                  cf='dasf12r1324', email='francesco@fadda.net', address=hkAddress,
                                  username='francesco', password=str(pbkdf2_sha256.encrypt("isw", rounds=12000,salt_size=32)))
        hotelKeeper.save()
        hotelAddress = Address(street='via hotel bellissimo', houseNumber=12, city='savona', zipCode='00929')
        hotelAddress.save()
        hotel = Hotel(name='Hotel Acquaragia', description='Hotel bellissimo', hotelKeeperId=hotelKeeper,
                      address=hotelAddress, photoUrl='/static/img/amsterdamHotel.jpg')
        hotel.save()
        service1 = IncludedService(service=IncludedService.GARAGE)
        service1.save()
        service2 = IncludedService(service=IncludedService.TELEPHONE)
        service2.save()
        room1 = Room(roomNumber=12, capacity=3, price=40.0, hotelId=hotel)
        room1.save()
        room1.services.add(service1)
        room2 = Room(roomNumber=14, capacity=3, price=60.0, hotelId=hotel)
        room2.save()
        room2.services.add(service2)
        hotel2 = Hotel(name='Hotel Napoleone', description='Hotel bellissimo', hotelKeeperId=hotelKeeper,
                       address=hotelAddress, photoUrl='/static/img/amsterdamHotel.jpg')
        hotel2.save()
        hotelKeeperNoHotels = HotelKeeper(name='fabrizio', surname='secci', birthday=datetime.date(1996, 10, 20),
                                          cf='dasf12r1324', email='fabrizio@secci.net', address=hkAddress,
                                          username='fabrizio', password=str(pbkdf2_sha256.encrypt("isw", rounds=12000,salt_size=32)))
        hotelKeeperNoHotels.save()

        self.userWithHotels = hotelKeeper
        self.userWithoutHotels = hotelKeeperNoHotels
        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def test_HotelListVisualization(self):
        request = self.request_factory.get('/hotels/')
        self.middleware.process_request(request)
        request.session.save()
        request.session['usr'] = self.userWithHotels.username
        request.session['usrType'] = 'hotelKeeper'
        response = hotelsList(request)
        self.assertContains(response, 'Hotel Acquaragia')
        self.assertContains(response, 'Hotel Napoleone')

    def test_EmptyHotelListVisualization(self):
        request = self.request_factory.get('/hotels/')
        self.middleware.process_request(request)
        request.session.save()
        request.session['usr'] = self.userWithoutHotels.username
        request.session['usrType'] = 'hotelKeeper'
        response = hotelsList(request)
        self.assertContains(response, "You have not registered any hotel!")


'''User story 5. add hotel'''


class AddHotelInTheList(TestCase):
    def setUp(self):
        hkAddress = Address(street='via del guasto', houseNumber=28, city='Bologna', zipCode='09888')
        hkAddress.save()
        hotelKeeper = HotelKeeper(name='Gianna', surname='Poho', birthday=datetime.date(1992, 1, 12),
                                  cf='phognn92t21b354ta', email='g.poho@gmail.com', address=hkAddress,
                                  username='giannina', password=str(pbkdf2_sha256.encrypt("isw", rounds=12000,salt_size=32)))
        hotelKeeper.save()
        h1Address = Address(street='via da qui', houseNumber=40, city='Bologna', zipCode='09888')
        h1Address.save()
        hotel1 = Hotel(name='Hotel Bacco', description="Nell'affascinante Bologna...", hotelKeeperId=hotelKeeper,
                       address=h1Address, photoUrl='/static/img/bedAndBreakfastLondon.jpg')
        hotel1.save()
        h2Address = Address(street='via Quadrilatero', houseNumber=90, city='Bologna', zipCode='09888')
        h2Address.save()
        hotel2 = Hotel(name='Hotel Tarallucci', description="Tanti biscotti a colazione", hotelKeeperId=hotelKeeper,
                       address=h2Address, photoUrl='/static/img/cortina.jpg')
        hotel2.save()
        newAddress = Address(street='via Holita', houseNumber=30, city='Bologna', zipCode='09888')
        newAddress.save()

        self.newAd = newAddress
        self.userhotelkeeper = hotelKeeper
        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def test_AddHotelInTheList(self):
        request = self.request_factory.get('/addHotel/', follow=True)
        self.middleware.process_request(request)
        request.session.save()
        request.session['usr'] = self.userhotelkeeper.username
        request.session['usrType'] = 'hotelKeeper'

        photo_file = open(os.path.dirname(__file__) + '/../static/img/cortina.jpg', 'rb')
        form_data = {'name': "hotel Trinciapollo",
                     'description': "Poulet e besciamel",
                     'street': self.newAd.street,
                     'houseNumber': self.newAd.houseNumber,
                     'city': self.newAd.city,
                     'zipCode': self.newAd.zipCode,
                     'photoUrl': SimpleUploadedFile(photo_file.name, photo_file.read())}

        form = AddHotelForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=form.errors)


"""Manage Hotel 6 controllo dettagli hotel e camera"""


class ManageHotel(TestCase):
    def setUp(self):
        hkAddress = Address(street='via francesco', houseNumber=12, city='savona', zipCode='00989')
        hkAddress.save()

        hotelKeeper = HotelKeeper(name='francesco', surname='fadda', birthday=datetime.date(1996, 10, 20),
                                  cf='dasf12r1324',
                                  email='francesco@fadda.net', address=hkAddress, username='francesco',
                                  password=str(pbkdf2_sha256.encrypt("isw", rounds=12000,salt_size=32)))
        hotelKeeper.save()

        hotelAddress = Address(street='via hotel bellissimo', houseNumber=12, city='savona', zipCode='00929')
        hotelAddress.save()

        hotel = Hotel(name='Hotel Acquaragia', description='Hotel bellissimo', hotelKeeperId=hotelKeeper,
                      address=hotelAddress,
                      photoUrl='/static/img/amsterdamHotel.jpg')
        hotel.save()

        room1 = Room(roomNumber=40, capacity=3, price='120', hotelId=hotel)

        room1.save()

        service = IncludedService(service=IncludedService.GARAGE, room=room1)

        service.save()

        self.hotelKeeperSession = hotelKeeper
        self.hotel = hotel
        self.hotelAddress = hotelAddress
        self.room = room1
        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def test_hotelsRoomsDataVisualization(self):
        hotelPage = '/hotel/?name=' + self.hotel.name + '&civN=' + str(
            self.hotelAddress.houseNumber) + '&city=' + self.hotelAddress.city
        request = self.request_factory.get(hotelPage, follow=True)
        self.middleware.process_request(request)
        request.session.save()
        request.session['usr'] = self.hotelKeeperSession.username
        request.session['usrType'] = 'hotelKeeper'

        response = hotelDetail(request)

        self.assertContains(response, 'Hotel Acquaragia')
        self.assertContains(response, '40')
        self.assertContains(response, '3')
        self.assertContains(response, '120')


'''User story 7. add a room to hotel'''


class AddRoomToHotelTest(TestCase):
    def setUp(self):
        hkAddress = Address(street='via del guasto', houseNumber=28, city='Bologna', zipCode='09888')
        hkAddress.save()
        hotelKeeper = HotelKeeper(name='Gianna', surname='Poho', birthday=datetime.date(1992, 1, 12),
                                  cf='phognn92t21b354ta', email='g.poho@gmail.com', address=hkAddress,
                                  username='giannina',password=str(pbkdf2_sha256.encrypt("isw", rounds=12000,salt_size=32)))
        hotelKeeper.save()
        h1Address = Address(street='via da qui', houseNumber=40, city='Bologna', zipCode='09888')
        h1Address.save()
        hotel = Hotel(name='Hotel Bacco', description="Nell'affascinante Bologna...", hotelKeeperId=hotelKeeper,
                      address=h1Address, photoUrl='/static/img/bedAndBreakfastLondon.jpg')
        hotel.save()

        self.userhotelkeeper = hotelKeeper
        self.hotel = hotel
        self.hotelAddress = hkAddress
        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def test_addRoomMissingFields(self):
        request = self.request_factory.get('/addRoom/', follow=True)
        self.middleware.process_request(request)
        request.session.save()

        request.session['htName'] = self.hotel.name
        request.session['htCivN'] = self.hotelAddress.houseNumber

        form = AddRoomForm(data={'roomNumber': 3, 'bedsNumber': 2})

        self.assertFalse(form.is_valid(), msg=form.errors)


"""user story 8. search"""


class SearchResultTest(TestCase):
    def setUp(self):
        hkAddress = Address(street='via francesco', houseNumber=12, city='savona', zipCode='00989')
        hkAddress.save()
        bookedUser = Client(name='gianni', surname='deGasperi', birthday=datetime.date(1996, 10, 20), cf='fsaf34f32',
                          email='gianni@gmail.com', address=hkAddress)
        bookedUser.save()
        userCreditCard = CreditCard(cardNumber='124563455436', expirationYear='2022', expirationMonth='03',
                                    cvvCode='007', owner=bookedUser)
        userCreditCard.save()
        hotelKeeper = HotelKeeper(name='francesco', surname='fadda', birthday=datetime.date(1996, 10, 20),
                                  cf='dasf12r1324', email='francesco@fadda.net', address=hkAddress,
                                  username='francesco', password=str(pbkdf2_sha256.encrypt("isw", rounds=12000,salt_size=32)))
        hotelKeeper.save()
        hotelAddress = Address(street='via hotel bellissimo', houseNumber=12, city='savona', zipCode='00929')
        hotelAddress.save()
        hotel = Hotel(name='Hotel Acquaragia', description='Hotel bellissimo', hotelKeeperId=hotelKeeper,
                      address=hotelAddress, photoUrl='/static/img/amsterdamHotel.jpg')
        hotel.save()
        bookedRoom = Room(roomNumber=12, capacity=3, price=40.0, hotelId=hotel)
        bookedRoom.save()
        hotelKeeperNoBookings = HotelKeeper(name='filippo', surname='podddesu', birthday=datetime.date(1996, 10, 20),
                                            cf='dasf12r1324', email='filippo@poddesu.net', address=hkAddress,
                                            username='filippo',password=str(pbkdf2_sha256.encrypt("isw", rounds=12000,salt_size=32)))
        hotelKeeperNoBookings.save()
        booking = Booking(customerId=bookedUser, roomId=bookedRoom, checkIn=datetime.date(2018, 11, 28),
                          checkOut=datetime.date(2018, 11, 20))
        booking.save()

        self.userWithHotels = hotelKeeper

        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def test_SearchResult(self):
        #   request = self.request_factory.get('/search/?search_city=savona&search_number=3&search_checkin=2018-06-15&search_checkout=2018-06-24', follow=True)
        request = self.request_factory.get('/search/', follow=True)

        request.GET.__init__(mutable=True)

        request.GET['search_city'] = 'savona'
        request.GET['search_number'] = '3'
        request.GET['search_checkin'] = '2018-01-01'
        request.GET['search_checkout'] = '2018-01-05'

        self.middleware.process_request(request)
        request.session.save()

        response = searchResults(request)

        self.assertContains(response, 'Hotel Acquaragia')

    def test_SearchError(self):
        #   request = self.request_factory.get('/search/?search_city=savona&search_number=3&search_checkin=2018-06-15&search_checkout=2018-06-24', follow=True)
        request = self.request_factory.get('/search/', follow=True)

        request.GET.__init__(mutable=True)

        request.GET['search_city'] = 'cagliari'
        request.GET['search_number'] = '3'
        request.GET['search_checkin'] = '2018-01-01'
        request.GET['search_checkout'] = '2018-01-05'

        self.middleware.process_request(request)
        request.session.save()

        response = searchResults(request)

        self.assertContains(response, 'There are no rooms available with these requirements')


'''User story 9. book a room'''


class reserveRoom(TestCase):
    def setUp(self):
        hkAddress = Address(street='via francesco', houseNumber=12, city='savona', zipCode='00989')
        hkAddress.save()

        hotelKeeper = HotelKeeper(name='francesco', surname='fadda', birthday=datetime.date(1996, 10, 20),
                                  cf='dasf12r1324',
                                  email='francesco@fadda.net', address=hkAddress, username='francesco',
                                  password=str(pbkdf2_sha256.encrypt("isw", rounds=12000,salt_size=32)))
        hotelKeeper.save()

        hotelAddress = Address(street='via hotel bellissimo', houseNumber=12, city='savona', zipCode='00929')
        hotelAddress.save()

        hotel = Hotel(name='Hotel Acquaragia', description='Hotel bellissimo', hotelKeeperId=hotelKeeper,
                      address=hotelAddress,
                      photoUrl='/static/img/amsterdamHotel.jpg')
        hotel.save()

        room1 = Room(roomNumber=40, capacity=3, price='120', hotelId=hotel)
        room1.save()

        service = IncludedService(service=IncludedService.GARAGE, room=room1)

        service.save()

        self.hotel = hotel
        self.hotelAddress = hotelAddress
        self.room = room1
        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def test_bookingMissingFields(self):
        # http://127.0.0.1:8000/booking/?roomid=4
        bookingPage = '/booking/?roomid=' + str(self.room.id)
        request = self.request_factory.get(bookingPage, follow=True)
        self.middleware.process_request(request)
        request.session.save()

        response = bookARoom(request)

        form = PaymentForm(data={
            'name': 'Giorgio',
            'surname': 'Imola',
            'birthday': '2018-10-21',
            'cf': '90913829011',
            'email': 'giogioImola@gmail.com',
            'username': 'giorgio',
            'password': 'isw',
            'verifyPassord': 'isw',
            'street': 'via dalle scatole',
            'civicNumber': '777',
            'city': 'Marius',
            'zipCode': '02131',
            # 'cardNumber': '123456789012345',
            'month': '10',
            'year': '2019',
            'cvv': '908'
        })
        self.assertFalse(form.is_valid(), msg=form.errors)


"""User story 10. data save when booking"""


class TestDatasave(TestCase):
    def setUp(self):
        hkAddress = Address(street='via francesco', houseNumber=12, city='savona', zipCode='00989')
        hkAddress.save()
        bookedUser = Client(name='gianni', surname='deGasperi', birthday=datetime.date(1996, 10, 20), cf='fsaf34f32',
                          email='gianni@gmail.com', address=hkAddress)
        bookedUser.save()
        userCreditCard = CreditCard(cardNumber='124563455436', expirationYear='2022', expirationMonth='03',
                                    cvvCode='007',
                                    owner=bookedUser)
        userCreditCard.save()
        hotelKeeper = HotelKeeper(name='francesco', surname='fadda', birthday=datetime.date(1996, 10, 20),
                                  cf='dasf12r1324',
                                  email='francesco@fadda.net', address=hkAddress, username='francesco',
                                  password=str(pbkdf2_sha256.encrypt("isw", rounds=12000,salt_size=32)))
        hotelKeeper.save()
        hotelAddress = Address(street='via hotel bellissimo', houseNumber=12, city='savona', zipCode='00929')
        hotelAddress.save()
        hotel = Hotel(name='Hotel Acquaragia', description='Hotel bellissimo', hotelKeeperId=hotelKeeper,
                      address=hotelAddress, photoUrl='/static/img/amsterdamHotel.jpg')
        hotel.save()
        bookedRoom = Room(roomNumber=12, capacity=3, price=40.0, hotelId=hotel)
        bookedRoom.save()
        hotelKeeperNoBookings = HotelKeeper(name='filippo', surname='podddesu',
                                            birthday=datetime.date(1996, 10, 20),
                                            cf='dasf12r1324', email='filippo@poddesu.net', address=hkAddress,
                                            username='filippo', password=str(pbkdf2_sha256.encrypt("isw", rounds=12000,salt_size=32)))
        hotelKeeperNoBookings.save()
        booking = Booking(customerId=bookedUser, roomId=bookedRoom, checkIn=datetime.date(2018, 11, 28),
                          checkOut=datetime.date(2018, 11, 20))
        booking.save()

        self.userWithHotels = hotelKeeper

        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def testSearchResult(self):
        form_data = {'name': 'Marco', 'surname': 'cognome',
                     'birthday': datetime.date(1996, 10, 20),
                     'cf': '23132123321', 'email': 'mail@ciao.com',
                     'street': 'via', 'civicNumber': 12, 'city': 'cagliari',
                     'zipCode': '09100', 'cardNumber': 788888999987900,
                     'month': 12, 'year': 2019, 'cvv': 321,
                     'username': 'miao', 'password': 'isw',
                     'verifyPassword': 'isw'}

        self.client.post('/booking/?roomid=1', form_data)

        app_count = RegisteredClient.objects.filter(username='miao').count()
        self.assertEqual(app_count, 1)




class AddHotel(TestCase):
    def setUp(self):
        hkAddress = Address(street='via francesco', houseNumber=12, city='savona', zipCode='00989')
        hkAddress.save()

        hotelKeeper = HotelKeeper(name='francesco', surname='fadda', birthday=datetime.date(1996, 10, 20),cf='dasf12r1324',
                                  email='francesco@fadda.net', address=hkAddress, username='francesco',
                                  password=str(pbkdf2_sha256.encrypt("isw", rounds=12000,salt_size=32)))
        hotelKeeper.save()

        hotelAddress = Address(street='via hotel bellissimo', houseNumber=12, city='savona', zipCode='00929')
        hotelAddress.save()

        hotel = Hotel(name='Hotel Acquaragia', description='Hotel bellissimo', hotelKeeperId=hotelKeeper,address=hotelAddress,
                      photoUrl='/static/img/amsterdamHotel.jpg')
        hotel.save()

        self.hotel = hotel
        self.hotelKeeper = hotelKeeper
        self.hotelAddress = hotelAddress
        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()


    def test_addHotel(self):
        listaHotel = []
        bookingPage = '/booking/addHotel/'
        request = self.request_factory.get(bookingPage, follow=True)
        self.middleware.process_request(request)
        session_key = self.hotelKeeper.username
        session = self.client.session
        session['usr'] = session_key
        session.save()

        for ht in Hotel.objects.all():
            if(ht.hotelKeeperId.username == self.hotelKeeper.username):
                listaHotel.append(ht)

        self.assertEqual(len(listaHotel),1)

        response = addHotel(request)

        form = AddHotelForm(data={
            'name': 'Bonsoir',
            'description': "C'est magnifique",
            'street': 'Rue Mont Poisson',
            'houseNumber': 5,
            'city': 'Paris',
            'zipCode': '09234',
            'photoUrl' : '/static/img/parisHotel.jpg'
        })

        form_data = {'name': 'Bonsoir','description': "C'est magnifique",'street': 'Rue Mont Poisson','houseNumber': 5,'city': 'Paris',
                     'zipCode': '09234','photoUrl' : '/static/img/parisHotel.jpg'}

        self.assertTrue(form.is_valid())

        self.assertEquals(response.status_code, 200)

        self.client.post('/addHotel/',form_data)

        listaHotel = []

        for ht in Hotel.objects.all():
            if(ht.hotelKeeperId.username == self.hotelKeeper.username):
                listaHotel.append(ht)

        self.assertEqual(len(listaHotel), 2)




class AddRoom(TestCase):
    def setUp(self):
        hkAddress = Address(street='via francesco', houseNumber=12, city='savona', zipCode='00989')
        hkAddress.save()

        hotelKeeper = HotelKeeper(name='francesco', surname='fadda', birthday=datetime.date(1996, 10, 20),cf='dasf12r1324',
                                  email='francesco@fadda.net', address=hkAddress, username='francesco',
                                  password=str(pbkdf2_sha256.encrypt("isw", rounds=12000,salt_size=32)))
        hotelKeeper.save()

        hotelAddress = Address(street='via hotel bellissimo', houseNumber=12, city='savona', zipCode='00929')
        hotelAddress.save()

        hotel = Hotel(name='Hotel Acquaragia', description='Hotel bellissimo', hotelKeeperId=hotelKeeper,address=hotelAddress,
                      photoUrl='/static/img/amsterdamHotel.jpg')
        hotel.save()

        room = Room(roomNumber=27,capacity=3,price=35.5,hotelId=hotel)
        room.save()

        self.hotel = hotel
        self.hotelKeeper = hotelKeeper
        self.hotelAddress = hotelAddress
        self.room = room
        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()



    def test_addRoom(self):
        roomList = []
        bookingPage = '/booking/addRoom/'
        request = self.request_factory.get(bookingPage, follow=True)
        self.middleware.process_request(request)
        session_key1 = str(self.hotel.name)
        session_key2 = str(self.hotel.address.houseNumber)
        session = self.client.session
        session['htName'] = session_key1
        session['htCivN'] = session_key2
        session.save()

        form = AddRoomForm(data={'roomNumber': 111,
                                 'bedsNumber': 3,
                                 'services' : ["TELEPHONE","GARAGE"],
                                 'price' : 75.50
                                 })

        self.assertTrue(form.is_valid())

        for rm in Room.objects.all():
            if (rm.hotelId == self.hotel):
                roomList.append(rm)

        self.assertEqual(len(roomList), 1)

        form_data = {'roomNumber': 111,'bedsNumber': 3,'services' : ["TELEPHONE","GARAGE"],'price' : 75.50}

        self.client.post('/addRoom/',form_data)

        roomList = []

        for rm in Room.objects.all():
            if (rm.hotelId == self.hotel):
                roomList.append(rm)

        self.assertEqual(len(roomList), 2)


class NonRegistration(TestCase):
    def setUp(self):
        address = Address(street='via francesco', houseNumber=12, city='savona', zipCode='00989')
        address.save()

        registeredClient = RegisteredClient(name='Marco',surname='Baldo',birthday=datetime.date(1984, 1, 15),
                                        cf='bldmrc84a15b354a',email='marco.baldo@gmail.com',
                                        address=address,username='marco',
                                            password=str(pbkdf2_sha256.encrypt("isw", rounds=12000,salt_size=32)))
        registeredClient.save()

        self.registeredClient = registeredClient
        self.address = address
        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def test_non_registration(self):
        registeredClientList = []
        bookingPage = '/booking/signUp/'
        request = self.request_factory.get(bookingPage, follow=True)
        self.middleware.process_request(request)
        session = self.client.session
        session.save()


        form = RegistrationForm(data={'name' : 'Marco',
                                      'surname' : 'Rossi',
                                      'birthday' : datetime.date(1996,11,15),
                                      'cf' : 'MRCRSS01345503',
                                      'email' : 'm.rossi@outlook.com',
                                      'username' : 'marco',
                                      'password' : 'isw',
                                      'verifyPassword' : 'isw',
                                      'street' : 'Via Marchi',
                                      'civicNumber' : 15,
                                      'city' : 'Roma',
                                      'zipCode' : '09134'
                                    })

        self.assertFalse(form.is_valid())

        for cl in RegisteredClient.objects.all():
            registeredClientList.append(cl)

        self.assertTrue(len(registeredClientList),1)

        form_data = {'name':'Marco','surname':'Rossi','birthday':datetime.date(1996,11,15),'cf':'MRCRSS01345503',
                     'email':'m.rossi@outlook.com','username':'marco','password' : 'isw',
                     'verifyPassword':'isw','street':'Via Marchi','civicNumber':15,'city':'Roma',
                     'zipCode':'09134'}

        self.client.post('/signUp/', form_data)

        registeredClientList = []

        for cl in RegisteredClient.objects.all():
            registeredClientList.append(cl)

        self.assertTrue(len(registeredClientList),1)


    def test_check_registration_fields(self):
        bookingPage = '/booking/signUp/'
        request = self.request_factory.get(bookingPage, follow=True)
        self.middleware.process_request(request)


        form_data = {'name':'Marco','surname':'Rossi','birthday':datetime.date(1996,11,15),'cf':'MRCRSS01345503',
                     'email':'m.rossi@outlook.com','username':'marco','password' : 'isw',
                     'verifyPassword':'isw','street':'Via Marchi','civicNumber':15,'city':'Roma',
                     'zipCode':'09134'}

        form = RegistrationForm(data=form_data)
        self.assertEqual(form.data['name'],"Marco")
        self.assertEqual(form.data['surname'],"Rossi")
        self.assertEqual(form.data['birthday'],datetime.date(1996,11,15))
        self.assertEqual(form.data['cf'],"MRCRSS01345503")
        self.assertEqual(form.data['email'],"m.rossi@outlook.com")
        self.assertEqual(form.data['username'],"marco")
        self.assertEqual(form.data['password'],"isw")
        self.assertEqual(form.data['verifyPassword'],"isw")
        self.assertEqual(form.data['street'],"Via Marchi")
        self.assertEqual(form.data['civicNumber'],15)
        self.assertEqual(form.data['city'],"Roma")
        self.assertEqual(form.data['zipCode'],"09134")