from django.test import TestCase
import enum
import unittest
import datetime
from .models import *


class ModelTest(TestCase):
    def setUp(self):
        person = Person(name = 'Stefano', surname = 'Usai', email = 'susai@gmail.com', birthday = '30/10/1984', cf = 'SUASFN84R30B354E')
        person.save()

        hotelKeeper = HotelKeeper( name = 'Giorgia', surname = 'Campanile', email = 'giogio.com', birthday = '16/10/96', cf = 'CMPGRG96R56')
        hotelKeeper.save()

        hotel = Hotel(name = 'T Hotel', description = 'Nel cuore di Cagliari...', town = 'Cagliari', OwnerID = 1)
        hotel.save()

        booking = Booking(idClient=123, idRoom = 123, checkIn = datetime.date(2012,12,15), checkOut = datetime.date(2012,12,35))