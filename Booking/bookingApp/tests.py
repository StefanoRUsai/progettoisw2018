from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, Client, RequestFactory
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


''''User story 4. (req. ViewHotelList)'''


class HotelsListTest(TestCase):
    def setUp(self):
        hkAddress = Address(
            street='via francesco',
            houseNumber=12,
            city='savona',
            zipCode='00989')
        hkAddress.save()

        hotelKeeper = HotelKeeper(
            name='francesco',
            surname='fadda',
            birthday=datetime.date(1996, 10, 20),
            cf='dasf12r1324',
            email='francesco@fadda.net',
            address=hkAddress,
            userName='francesco',
            password='isw'
        )
        hotelKeeper.save()

        hotelAddress = Address(
            street='via hotel bellissimo',
            houseNumber=12,
            city='savona',
            zipCode='00929')
        hotelAddress.save()

        hotel = Hotel(
            name='Hotel Acquaragia',
            description='Hotel bellissimo',
            hotelKeeperId=hotelKeeper,
            address=hotelAddress,
            photoUrl='/static/img/amsterdamHotel.jpg')
        hotel.save()

        service1 = IncludedService(
            service=IncludedService.GARAGE
        )

        service1.save()

        service2 = IncludedService(
            service=IncludedService.TELEPHONE
        )
        service2.save()

        room1 = Room(
            roomNumber=12,
            capacity=3,
            price=40.0,
            hotelId=hotel
        )

        room1.save()
        room1.services.add(service1)

        room2 = Room(
            roomNumber=14,
            capacity=3,
            price=60.0,
            hotelId=hotel
        )

        room2.save()
        room2.services.add(service2)

        hotel2 = Hotel(
            name='Hotel Napoleone',
            description='Hotel bellissimo',
            hotelKeeperId=hotelKeeper,
            address=hotelAddress,
            photoUrl='/static/img/amsterdamHotel.jpg')
        hotel2.save()

        hotelKeeperNoHotels = HotelKeeper(
            name='fabrizio',
            surname='secci',
            birthday=datetime.date(1996, 10, 20),
            cf='dasf12r1324',
            email='fabrizio@secci.net',
            address=hkAddress,
            userName='fabrizio',
            password='isw'
        )
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

        response = hotelsList(request)

        # print(response.status_code)
        self.assertContains(response, 'Hotel Acquaragia')
        self.assertContains(response, 'Hotel Napoleone')

    def testEmptyHotelListVisualization(self):
        request = self.request_factory.get('/hotels/')
        self.middleware.process_request(request)
        request.session.save()

        request.session['usr'] = self.userWithHotels.userName

        response = hotelsList(request)

        # print(response.status_code)
    #   self.assertContains(response, "You didn't register an hotel yet")


''''User story 1. (req. account hotelkeeper)'''
""" simulazione in black box mode """


class RegistrationHotelKeeperTest(TestCase):
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
            userName='ele',
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

    def testHomeRegisteredUserVizualization(self):
        request = self.request_factory.get('/login/', follow=True)
        self.middleware.process_request(request)
        request.session.save()

        request.session['usr'] = self.userregistered.userName
        request.session['usrType'] = 'regUser'

        response = login(request)

        print(request.get_full_path())
        print(response.status_code)

        self.assertEquals(response.status_code, 302)

    def testHomeHotelKeeperVizualization(self):
        request = self.request_factory.get('/login/', follow=True)
        self.middleware.process_request(request)
        request.session.save()

        request.session['usr'] = self.userhotelkeeper.userName
        request.session['usrType'] = 'hotelKeeper'

        response = login(request)

        print(request.get_full_path())
        print(response.status_code)

        self.assertEquals(response.status_code, 302)


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

        AddHotelForm.name = "hotel Trinciapollo"
        AddHotelForm.description = "Poulet e besciamel"
        AddHotelForm.street = self.newAd.street
        AddHotelForm.houseNumber = self.newAd.houseNumber
        AddHotelForm.city = self.newAd.city
        AddHotelForm.zipCode = self.newAd.zipCode
        AddHotelForm.photoUrl = "cortina.jpg"

        form_data ={'name': "hotel Trinciapollo",
                                  'description': "Poulet e besciamel",
                                  'street': self.newAd.street,
                                  'houseNumber': self.newAd.houseNumber,
                                  'city': self.newAd.city,
                                  'zipCode': self.newAd.zipCode,
                                  'photoUrl': "cortina.jpg"

                   }
        form = AddHotelForm(data=form_data)

        self.assertEqual(form.name, "hotel Trinciapollo")
        self.assertEqual(form.description, "Poulet e besciamel")
        self.assertEqual(form.street, "via Holita")
        self.assertEqual(form.houseNumber, self.newAd.houseNumber)
        self.assertEqual(form.city, self.newAd.city)
        self.assertEqual(form.zipCode, self.newAd.zipCode)
        self.assertEqual(form.photoUrl, "cortina.jpg")










