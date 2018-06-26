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


class ModelTest(TestCase):
    def setUp(self):
        addressGlobal = Address(
            street='via Piave',
            houseNumber=60,
            city='Uras',
            zipCode='78999')

        addressGlobal.save()

        creditCardGlobal = CreditCard(
            cardNumber=56478397474839375,
            expirationMonth=12,
            expirationYear=2020,
            cvvCode=666)

        creditCardGlobal.save()

        creditCard = CreditCard(
            cardNumber=788888999987900,
            expirationMonth=10,
            expirationYear=2019,
            cvvCode=555)

        creditCard.save()

        person = Person(
            name='Stefano',
            surname='Marcello',
            email='smarcello@gmail.com',
            birthday=datetime.date(1987, 10, 11),
            cf='MRCSTN84S13A355X',
            address=addressGlobal)

        person.save()

        hotelKeeper = HotelKeeper(
            name='Giorgia',
            surname='Congiu',
            email='giogio.com',
            birthday=datetime.date(1996, 10, 20),
            cf='CNGGRG96R60A355U',
            userName='giogioCong96',
            password='palazzodellescienze',
            address=addressGlobal)

        hotelKeeper.save()

        hotel = Hotel(
            name='T Hotel',
            description='Nel cuore di Cagliari...',
            hotelKeeperId=hotelKeeper,
            address=addressGlobal)

        hotel.save()

        room1 = Room(
            capacity=3,
            price='120.00',
            hotelId=hotel)

        room1.save()

        service = IncludedService(service=IncludedService.GARAGE, room=room1)

        service.save()

        user = User(
            name='Carlo',
            surname='Puddu',
            email='cpuddu@gmail.com',
            birthday=datetime.date(1990, 10, 6),
            cf='PDDCRL90F06F979T',
            address=addressGlobal,
            creditCard=creditCardGlobal)

        user.save()

        registeredUser = RegisteredUser(
            name='Mario',
            surname='Cittadini',
            email='marcit@gmail.com',
            birthday=datetime.date(1987, 10, 11),
            cf='CTTMRA76T607T',
            userName='marcittttt2018',
            password='gitPullFailed',
            address=addressGlobal,
            creditCard=creditCardGlobal)

        registeredUser.save()

        booking = Booking(
            customerId=user,
            roomId=room1,
            checkIn=datetime.date(2018, 11, 12),
            checkOut=datetime.date(2018, 11, 18))

        booking.save()


'''User story 3. Visualizza lista prenotazioni (hotelKeeperhome)'''
class HotelKeeperHome(TestCase):
    def setUp(self):
        hkAddress = Address(street='via francesco',houseNumber=12,city='savona',zipCode='00989')
        hkAddress.save()
        bookedUser = User(name='gianni', surname='deGasperi',birthday=datetime.date(1996,10,20),cf='fsaf34f32', email='gianni@gmail.com',address=hkAddress)
        bookedUser.save()
        userCreditCard=CreditCard(cardNumber='124563455436',expirationYear='2022',expirationMonth='03',cvvCode='007',owner=bookedUser)
        userCreditCard.save()
        hotelKeeper = HotelKeeper(name='francesco',surname='fadda',birthday= datetime.date(1996,10,20),cf='dasf12r1324',email='francesco@fadda.net',address=hkAddress,userName='francesco',password='isw')
        hotelKeeper.save()
        hotelAddress = Address(street='via hotel bellissimo',houseNumber=12,city='savona',zipCode='00929')
        hotelAddress.save()
        hotel = Hotel(name='Hotel Acquaragia',description='Hotel bellissimo',hotelKeeperId=hotelKeeper,address=hotelAddress,photoUrl='/static/img/amsterdamHotel.jpg')
        hotel.save()
        bookedRoom = Room(roomNumber=12,capacity=3,price=40.0,hotelId=hotel)
        bookedRoom.save()
        hotelKeeperNoBookings = HotelKeeper(name='filippo',surname='podddesu',birthday=datetime.date(1996,10,20),cf='dasf12r1324',email='filippo@poddesu.net',address=hkAddress,userName='filippo',password='isw')
        hotelKeeperNoBookings.save()
        booking = Booking(customerId=bookedUser,roomId=bookedRoom,checkIn=datetime.date(2018,11,28),checkOut=datetime.date(2018,11,20))
        booking.save()

        self.userWithBookings = hotelKeeper
        self.userWithoutBookings = hotelKeeperNoBookings
        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def test_hotelKeeperBookingsVisualization(self):
        request = self.request_factory.get('/home/')
        self.middleware.process_request(request)
        request.session.save()
        request.session['usr'] = self.userWithBookings.userName
        request.session['usrType'] = 'hotelKeeper'
        response = hotelKeeperHome(request)
        self.assertContains(response,'gianni')
        self.assertContains(response,'Hotel Acquaragia')

    def test_hotelKeeperNoBookingsMessage(self):
        request = self.request_factory.get('/home/')
        self.middleware.process_request(request)
        request.session.save()
        request.session['usr'] = self.userWithoutBookings.userName
        request.session['usrType'] = 'hotelKeeper'
        response = hotelKeeperHome(request)
        self.assertContains(response, "You have not reservations in your hotels!")




''''User story 4. (req. ViewHotelList)'''
class HotelsListTest(TestCase):
    def setUp(self):
        hkAddress = Address(street='via francesco',houseNumber=12,city='savona',zipCode='00989')
        hkAddress.save()
        hotelKeeper = HotelKeeper(name='francesco',surname='fadda',birthday=datetime.date(1996, 10, 20),cf='dasf12r1324',email='francesco@fadda.net',address=hkAddress,userName='francesco',password='isw')
        hotelKeeper.save()
        hotelAddress = Address(street='via hotel bellissimo',houseNumber=12,city='savona',zipCode='00929')
        hotelAddress.save()
        hotel = Hotel(name='Hotel Acquaragia',description='Hotel bellissimo',hotelKeeperId=hotelKeeper,address=hotelAddress,photoUrl='/static/img/amsterdamHotel.jpg')
        hotel.save()
        service1 = IncludedService(service=IncludedService.GARAGE)
        service1.save()
        service2 = IncludedService(service=IncludedService.TELEPHONE)
        service2.save()
        room1 = Room(roomNumber=12,capacity=3,price=40.0,hotelId=hotel)
        room1.save()
        room1.services.add(service1)
        room2 = Room(roomNumber=14,capacity=3,price=60.0,hotelId=hotel)
        room2.save()
        room2.services.add(service2)
        hotel2 = Hotel(name='Hotel Napoleone',description='Hotel bellissimo',hotelKeeperId=hotelKeeper,address=hotelAddress,photoUrl='/static/img/amsterdamHotel.jpg')
        hotel2.save()
        hotelKeeperNoHotels = HotelKeeper(name='fabrizio',surname='secci',birthday=datetime.date(1996, 10, 20),cf='dasf12r1324',email='fabrizio@secci.net',address=hkAddress,userName='fabrizio',password='isw')
        hotelKeeperNoHotels.save()

        self.userWithHotels = hotelKeeper
        self.userWithoutHotels = hotelKeeperNoHotels
        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def testHotelListVisualization(self):
        request = self.request_factory.get('/hotels/')
        self.middleware.process_request(request)
        request.session.save()
        request.session['usr'] = self.userWithHotels.userName
        request.session['usrType'] = 'hotelKeeper'
        response = hotelsList(request)
        self.assertContains(response, 'Hotel Acquaragia')
        self.assertContains(response, 'Hotel Napoleone')

    def testEmptyHotelListVisualization(self):
        request = self.request_factory.get('/hotels/')
        self.middleware.process_request(request)
        request.session.save()
        request.session['usr'] = self.userWithoutHotels.userName
        request.session['usrType'] = 'hotelKeeper'
        response = hotelsList(request)
        self.assertContains(response, "You have not registered any hotel!")



class AddHotelInTheList(TestCase):

    def setUp(self):
        hkAddress = Address(
            street='via del guasto',
            houseNumber=28,
            city='Bologna',
            zipCode='09888')
        hkAddress.save()

        hotelKeeper = HotelKeeper(
            name='Gianna',
            surname='Poho',
            birthday=datetime.date(1992, 1, 12),
            cf='phognn92t21b354ta',
            email='g.poho@gmail.com',
            address=hkAddress,
            userName='giannina',
            password='isw'
        )
        hotelKeeper.save()

        h1Address = Address(
            street='via da qui',
            houseNumber=40,
            city='Bologna',
            zipCode='09888')
        h1Address.save()

        hotel1 = Hotel(
            name='Hotel Bacco',
            description="Nell'affascinante Bologna...",
            hotelKeeperId=hotelKeeper,
            address=h1Address,
            photoUrl='/static/img/bedAndBreakfastLondon.jpg'
        )
        hotel1.save()

        h2Address = Address(
            street='via Quadrilatero',
            houseNumber=90,
            city='Bologna',
            zipCode='09888')
        h2Address.save()

        hotel2 = Hotel(
            name='Hotel Tarallucci',
            description="Tanti biscotti a colazione",
            hotelKeeperId=hotelKeeper,
            address=h2Address,
            photoUrl='/static/img/cortina.jpg'
        )
        hotel2.save()

        newAddress = Address(
            street='via Holita',
            houseNumber=30,
            city='Bologna',
            zipCode='09888')
        newAddress.save()

        self.newAd = newAddress
        self.userhotelkeeper = hotelKeeper
        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def testAddHotelInTheList(self):

        request = self.request_factory.get('/addHotel/', follow=True)
        self.middleware.process_request(request)
        request.session.save()
        request.session['usr'] = self.userhotelkeeper.userName
        request.session['usrType'] = 'hotelKeeper'


        photo_file = open(os.path.dirname(__file__)+'/../static/img/cortina.jpg', 'rb')
        form_data ={'name': "hotel Trinciapollo",
                                  'description': "Poulet e besciamel",
                                  'street': self.newAd.street,
                                  'houseNumber': self.newAd.houseNumber,
                                  'city': self.newAd.city,
                                  'zipCode': self.newAd.zipCode,
                                  'photoUrl': SimpleUploadedFile(photo_file.name, photo_file.read())}


        form = AddHotelForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=form.errors)



"""test login"""
class LoginHotelKeeperTest(TestCase):
    def setUp(self):
        address = Address(
            street='via lanusei',
            houseNumber=12,
            city='Cagliari',
            zipCode='09127')
        address.save()

        hotelKeeper = HotelKeeper(
            name='Elena',
            surname='Puddu',
            birthday=datetime.date(1980, 1, 1),
            cf='pdueln80a21b354a',
            email='e.puddu@gmail.com',
            address=address,
            userName='prova23',
            password='isw'
        )

        address = Address(
            street='via nuoro',
            houseNumber=16,
            city='Cagliari',
            zipCode='09127')
        address.save()

        registereduser = RegisteredUser(
            name='Marco',
            surname='Baldo',
            birthday=datetime.date(1984, 1, 15),
            cf='bldmrc84a15b354a',
            email='marco.baldo@gmail.com',
            address=address,
            userName='baldo',
            password='isw'
        )
        hotelKeeper.save()
        registereduser.save()

        self.userregistered = registereduser
        self.userhotelkeeper = hotelKeeper
        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def testLoginPageRedirect(self):
        request = self.request_factory.get('/login/', follow=True)
        self.middleware.process_request(request)
        request.session.save()

        request.session['usr'] = self.userhotelkeeper.userName
        request.session['usrType'] = 'hotelKeeper'

        response = login(request)

        print(request.get_full_path())
        print(response.status_code)

        self.assertEquals(response.status_code, 302)

    def testLoginHotelKeeper(self):
        form = formLogin(data={'username': self.userhotelkeeper.userName,
                               'password': self.userhotelkeeper.password})

        self.assertTrue(form.is_valid(), msg=form.errors)

    def testLoginRegisteredUser(self):
        form = formLogin(data={'username': self.userregistered.userName,
                               'password': self.userregistered.password})

        self.assertTrue(form.is_valid(), msg=form.errors)



""" registrazione utente, controllo visualizzazione pagina home"""
class RegisteredHotelKeeperTest(TestCase):

    def setUp(self):
        address = Address(
            street='via lanusei',
            houseNumber=12,
            city='Cagliari',
            zipCode='09127')
        address.save()

        hotelKeeper = HotelKeeper(
            name='Elena',
            surname='Puddu',
            birthday=datetime.date(1980, 1, 1),
            cf='pdueln80a21b354a',
            email='e.puddu@gmail.com',
            address=address,
            userName='prova23',
            password='isw'
        )

        address = Address(
            street='via nuoro',
            houseNumber=16,
            city='Cagliari',
            zipCode='09127')
        address.save()

        registereduser = RegisteredUser(
            name='Marco',
            surname='Baldo',
            birthday=datetime.date(1984, 1, 15),
            cf='bldmrc84a15b354a',
            email='marco.baldo@gmail.com',
            address=address,
            userName='baldo',
            password='isw'
        )
        hotelKeeper.save()
        registereduser.save()

        self.userregistered = registereduser
        self.userhotelkeeper = hotelKeeper
        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def testRegistrationHotelKeeper(self):

        request = self.request_factory.get('/signUp/', follow=True)
        self.middleware.process_request(request)
        request.session.save()

        form = RegistrationForm(data={'hotelKeeper': True
        ,'name': 'Pinco'
        ,'surname': 'Panco'
        ,'birthday': '2018-10-21'
        ,'cf': '213321321312'
        ,'email': 'baldo@gmail.com'
        ,'userName': 'pinco'
        ,'password': 'isw'
        ,'verificapassword': 'isw'
        ,'street': 'via da qui'
        ,'civicNumber': '666'
        ,'city': 'chenonce'
        ,'zipCode': '02131'})

        self.assertTrue(form.is_valid(), msg=form.errors)

    def testHomeHotellKeeper(self):
        request = self.request_factory.get('/home/', follow=True)
        self.middleware.process_request(request)
        request.session.save()

        request.session['usr'] = 'prova23'
        request.session['usrType'] = 'hotelKeeper'

        response = hotelKeeperHome(request)

        self.assertEquals(response.status_code, 200)

    def testHomeHotellKeeperError(self):
        request = self.request_factory.get('/home/', follow=True)
        self.middleware.process_request(request)
        request.session.save()

        request.session['usr'] = 'baldo'
        request.session['usrType'] = 'regUser'

        response = hotelKeeperHome(request)

        self.assertEquals(response.status_code, 302)
