from django.db import models
from enum import Enum


# Create your models here.

class CreditCard(models.Model):
    cardNumber = models.CharField(max_length=10)
    expirationYear = models.CharField(max_length=4)
    expirationMonth = models.CharField(max_length=2)
    cvvCode = models.CharField(max_length=3)

    def __unicode__(self):
       return self.cardNumber + self.expirationYear + self.expirationMonth + self.cvvCode


class Address(models.Model):
    street = models.CharField(max_length=100)
    houseNumber = models.IntegerField()
    city = models.CharField(max_length=30)
    zipCode = models.CharField(max_length=15)

    def __unicode__(self):
       return self.street + self.houseNumber + self.city + self.zipCode
    def cityReturn(self):
        return self.city

class Person(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    birthday = models.DateField()
    cf = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)


class User(Person):
    creditCard = models.ForeignKey(CreditCard, on_delete=models.CASCADE, null=True)


class HotelKeeper(Person):
    userName = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __unicode__(self):
       return self.name + self.surname

class RegisteredUser(User):
    userName = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __unicode__(self):
       return self.name + self.surname + "...con username --> " + self.userName

class Hotel(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    hotelKeeperId = models.ForeignKey(HotelKeeper, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    photoUrl = models.ImageField(default=None, null=True, upload_to="static/img")

    def __unicode__(self):
       return self.name + self.address




class Room(models.Model):
    roomNumber = models.IntegerField(default=0)
    capacity = models.IntegerField(default=0)
    price = models.FloatField(default=0.0)
    hotelId = models.ForeignKey(Hotel, on_delete=models.CASCADE)

    def __unicode__(self):
       return "Hotel di appartenenza -->" + self.hotelId + "Room number --> " + self.roomNumber

class Booking(models.Model):
    customerId = models.ForeignKey(User, on_delete=models.CASCADE)
    roomId = models.ForeignKey(Room, on_delete=models.CASCADE)
    checkIn = models.DateField()
    checkOut = models.DateField()


class IncludedService(models.Model):
    NONE = 'NONE'
    TELEPHONE = 'TELEPHONE'
    GARAGE = 'GARAGE'
    WIFI = 'WIFI'
    BREAKFAST = 'BREAKFAST'
    LUNCH = 'LUNCH'
    DINNER = 'DINNER'
    BRUNCH = 'BRUNCH'

    availableServices = (
        (NONE, "No services"),
        (TELEPHONE, "Telephone"),
        (GARAGE, "Garage"),
        (WIFI, "Wifi"),
        (BREAKFAST, "Breakfast"),
        (LUNCH, "Lunch"),
        (DINNER, "Dinner"),
        (BRUNCH, "Brunch")
    )

    service = models.CharField(max_length=100, choices=availableServices, default=NONE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
