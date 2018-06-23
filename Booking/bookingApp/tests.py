from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, Client, RequestFactory
import enum
import unittest
import datetime
from .models import *


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
            cardNumber = 788888999987900,
            expirationMonth = 10,
            expirationYear = 2019,
            cvvCode = 555)

        creditCard.save()

        person = Person(
            name = 'Stefano',
            surname = 'Marcello',
            email = 'smarcello@gmail.com',
            birthday = datetime.date(1987,10,11),
            cf = 'MRCSTN84S13A355X',
            address = addressGlobal)

        person.save()

        hotelKeeper = HotelKeeper(
            name = 'Giorgia',
            surname = 'Congiu',
            email = 'giogio.com',
            birthday = datetime.date(1996,10,20),
            cf = 'CNGGRG96R60A355U',
            userName='giogioCong96',
            password='palazzodellescienze',
            address=addressGlobal)

        hotelKeeper.save()

        hotel = Hotel(
            name = 'T Hotel',
            description = 'Nel cuore di Cagliari...',
            hotelKeeperId = hotelKeeper,
            address = addressGlobal)

        hotel.save()

        room1 = Room(
            capacity=3,
            price='120.00',
            hotelId = hotel)

        room1.save()

        service = IncludedService(service=IncludedService.GARAGE, room=room1)

        service.save()



        user = User(
            name = 'Carlo',
            surname = 'Puddu',
            email = 'cpuddu@gmail.com',
            birthday = datetime.date(1990,10,6),
            cf = 'PDDCRL90F06F979T',
            address = addressGlobal,
            creditCard = creditCardGlobal)

        user.save()

        registeredUser = RegisteredUser(
            name = 'Mario',
            surname = 'Cittadini',
            email='marcit@gmail.com',
            birthday=datetime.date(1987,10,11),
            cf = 'CTTMRA76T607T',
            userName = 'marcittttt2018',
            password = 'gitPullFailed',
            address=addressGlobal,
            creditCard=creditCardGlobal)

        registeredUser.save()

        booking = Booking(
            customerId=user,
            roomId=room1,
            checkIn=datetime.date(2018, 11, 12),
            checkOut = datetime.date(2018, 11, 18))

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
            birthday= datetime.date(1996,10,20),
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
            service = IncludedService.GARAGE
        )

        service1.save()

        service2 = IncludedService(
            service = IncludedService.TELEPHONE
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
            birthday= datetime.date(1996,10,20),
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