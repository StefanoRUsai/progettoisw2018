from django.test import TestCase
import enum
import unittest
from .models import *
import datetime


class ModelTest(TestCase):
    def setUp(self):
        person = Person(name = 'Stefano', surname = 'Usai', email = 'susai@gmail.com', birthday = '30/10/1984', cf = 'SUASFN84R30B354E')
        person.save()

        hotelKeeper = HotelKeeper( name = 'Giorgia', surname = 'Campanile', email = 'giogio.com', birthday = '16/10/96', cf = 'CMPGRG96R56')
        hotelKeeper.save()

        hotel = Hotel(name = 'T Hotel', description = 'Nel cuore di Cagliari...', town = 'Cagliari', OwnerID = 1)
        hotel.save()

        booking = Booking(clientId = 1234, ownerId = 1234, checkIn = datetime.date(2018,11,12), checkOut = datetime.date(2018,11,18))