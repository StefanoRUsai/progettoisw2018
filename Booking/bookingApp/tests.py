from django.test import TestCase
import enum
import unittest
import datetime
from .models import *


class ModelTest(TestCase):
    def setUp(self):
        address = Address(street = 'via Piave', houseNumber =  60, town = 'Uras', postalCode = '78999')
        address.save()

        creditCard = CreditCard(cardNumber = 788888999987900, month = 10, year = 2019, CVV = 555)
        creditCard.save()

        person = Person(name = 'Stefano', surname = 'Marcello', email = 'smarcello@gmail.com', birthday = '13/09/1984', cf = 'MRCSTN84S13A355X',
                        address = Address(street = 'via Giardini', houseNumber = 29, town = 'Muravera', postalCode = '09043'))
        person.save()

        hotelKeeper = HotelKeeper( name = 'Giorgia', surname = 'Congiu', email = 'giogio.com', birthday = '20/10/96', cf = 'CNGGRG96R60A355U',
                                   userName='giogioCong96', psw='palazzodellescienze',
                                   address=Address(street='via Ciusa', houseNumber=80, town='Villaputzu',
                                                   postalCode='00000'))
        hotelKeeper.save()

        hotel = Hotel(name = 'T Hotel', description = 'Nel cuore di Cagliari...', town = 'Cagliari', OwnerID = 1,
                      address = Address(street = 'via Manlio', houseNumber = 90, town = 'QuartuSE', postalCode = '99090'))
        hotel.save()

        room = Room(nBeds=3, price='120.00', services = Service.BREAKFAST, HotelID = 2)
        room.save()

        user = User(name = 'Carlo', surname = 'Puddu', email = 'cpuddu@gmail.com', birthday = '06/10/1990',
                        cf = 'PDDCRL90F06F979T', address = Address('via degli Ulivi', '129', 'Mandas', '09040'),
                        creditCard = CreditCard(cardNumber = 56478397474839375, month = 12, year = 2020, CVV = 666))
        user.save()

        registeredUser = RegisteredUser(name = 'Mario', surname = 'Cittadini', email='marcit@gmail.com', birthday='10/10/76',
                                  cf = 'CTTMRA76T607T', userName = 'marcittttt2018', psw = 'gitPullFailed',
                                    address=Address('via dei Canneti', '199', 'Musei', '09088'),
                                    creditCard=CreditCard(cardNumber=56478666666665, month=5, year=2021,CVV=906))
        registeredUser.save()

        booking = Booking(clientId=1234, ownerId=1234, checkIn=datetime.date(2018, 11, 12),
                          checkOut = datetime.date(2018, 11, 18))
        booking.save()





