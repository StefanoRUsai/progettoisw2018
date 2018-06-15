from django.test import TestCase
import enum from Enum
import unittest
from .models import *


class ModelTest(TestCase):
    def setUp(self):
        person = Person(name = 'Stefano', surname = 'Marcello', email = 'smarcello@gmail.com', birthday = '13/09/1984', cf = 'MRCSTN84S13A355X',
                        address = Address('via Giardini', 29, 'Muravera', '04093'))
        person.save()

        hotelKeeper = HotelKeeper( name = 'Giorgia', surname = 'Congiu', email = 'giogio.com', birthday = '20/10/96', cf = 'CNGGRG96R60A355U')
        hotelKeeper.save()

        hotel = Hotel(name = 'T Hotel', description = 'Nel cuore di Cagliari...', town = 'Cagliari', OwnerID = 1)
        hotel.save()

        room = Room(nBeds=3, price='120.00', services='breakfast', HotelID = 2)
        room.save()

        user = User(name = 'Carlo', surname = 'Puddu', email = 'cpuddu@gmail.com', birthday = '06/10/1990',
                        cf = 'PDDCRL90F06F979T', address = Address('via degli Ulivi', '129', 'Mandas', '09040'),
                        creditCard = CreditCard(56478397474839375, 12, 2020, 666))
        user.save()



