from django.test import TestCase
import enum
import unittest
import datetime
from .models import *


class ModelTest(TestCase):
    def setUp(self):

        print("inizio")

        address = Address(
            street = 'via Piave',
            houseNumber =  60,
            city= 'Uras',
            zipCode = '78999')

        address.save()

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
            birthday = '13/09/1984',
            cf = 'MRCSTN84S13A355X',
            address = Address(
                street = 'via Giardini',
                houseNumber = 29,
                city= 'Muravera',
                zipCode = '09043'))

        person.save()

        hotelKeeper = HotelKeeper(
            name = 'Giorgia',
            surname = 'Congiu',
            email = 'giogio.com',
            birthday = '20/10/96',
            cf = 'CNGGRG96R60A355U',
            userName='giogioCong96',
            password='palazzodellescienze',
            address=Address(
                street='via Ciusa',
                houseNumber=80,
                city='Villaputzu',
                zipCode='00000'))

        hotelKeeper.save()

        hotel = Hotel(
            name = 'T Hotel',
            description = 'Nel cuore di Cagliari...',
            city = 'Cagliari',
            hotelKeeperId = 1,
            address = Address(
                street = 'via Manlio',
                houseNumber = 90,
                city = 'QuartuSE',
                zipCode = '99090'))

        hotel.save()

        room = Room(
            capacity=3,
            price='120.00',
            hotelId = 2)

        room.save()

        service = Service(ServicesEnum.GARAGE, room)

        service.save()

        print(str(Service.objects.all()))
        for o in Service.objects.all().values():
            print(o)



        user = User(
            name = 'Carlo',
            surname = 'Puddu',
            email = 'cpuddu@gmail.com',
            birthday = '06/10/1990',
            cf = 'PDDCRL90F06F979T',
            address = Address('via degli Ulivi', '129', 'Mandas', '09040'),
            creditCard = CreditCard(
                cardNumber = 56478397474839375,
                expirationMonth = 12,
                expirationYear = 2020,
                cvvCode = 666))

        user.save()

        registeredUser = RegisteredUser(
            name = 'Mario',
            surname = 'Cittadini',
            email='marcit@gmail.com',
            birthday='10/10/76',
            cf = 'CTTMRA76T607T',
            userName = 'marcittttt2018',
            password = 'gitPullFailed',
            address=Address(
                'via dei Canneti',
                '199',
                'Musei',
                '09088'),
            creditCard=CreditCard(
                cardNumber=56478666666665,
                expirationMonth=5,
                expirationYear=2021,
                cvvCode=906))

        registeredUser.save()

        booking = Booking(
            customerId=1234,
            ownerId=1234,
            checkIn=datetime.date(2018, 11, 12),
            checkOut = datetime.date(2018, 11, 18))

        booking.save()





