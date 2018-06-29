from django.db import models
from enum import Enum


class Address(models.Model):
    street = models.CharField(max_length=100)
    houseNumber = models.IntegerField()
    city = models.CharField(max_length=30)
    zipCode = models.CharField(max_length=15)

    def __str__(self):
       return str(self.street) + " " + str(self.houseNumber) + " " + str(self.city) + " " + str(self.zipCode)



class Person(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    birthday = models.DateField()
    cf = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name) + " " + str(self.surname) + " " + str(self.birthday) + " " + str(self.cf) + " " + str(self.email) + " " + self.address.__str__()

class User(Person):
    phoneNumber = models.CharField(max_length=20)

    def __str__(self):
        return self.phoneNumber.__str__()



class CreditCard(models.Model):
    cardNumber = models.CharField(max_length=10)
    expirationYear = models.CharField(max_length=4)
    expirationMonth = models.CharField(max_length=2)
    cvvCode = models.CharField(max_length=3)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
       return str(self.cardNumber) + " " + str(self.expirationYear) + " " + str(self.expirationMonth) + " " + str(self.cvvCode)




class HotelKeeper(Person):
    userName = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
       return str(self.name) + " " + str(self.surname)

class RegisteredUser(User):
    userName = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
       return str(self.userName) # + " " + str(self.surname) + " ...con username --> " + str(self.userName)

class Hotel(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    hotelKeeperId = models.ForeignKey(HotelKeeper, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    photoUrl = models.ImageField(default=None, null=True, upload_to="static/img")

    def __str__(self):
       return str(self.name) + " " + self.address.__str__()

    def returnCity(self):
        return self.city


class IncludedService(models.Model):
    TELEPHONE = 'TELEPHONE'
    GARAGE = 'GARAGE'
    WIFI = 'WIFI'
    BREAKFAST = 'BREAKFAST'
    LUNCH = 'LUNCH'
    DINNER = 'DINNER'
    BRUNCH = 'BRUNCH'

    availableServices = (
        (TELEPHONE, "Telephone"),
        (GARAGE, "Garage"),
        (WIFI, "Wifi"),
        (BREAKFAST, "Breakfast"),
        (LUNCH, "Lunch"),
        (DINNER, "Dinner"),
        (BRUNCH, "Brunch")
    )

    service = models.CharField(max_length=100, choices=availableServices)

    def __str__(self):
        return self.service.__str__()


class Room(models.Model):
    roomNumber = models.IntegerField(default=0)
    capacity = models.IntegerField(default=0)
    price = models.FloatField(default=0.0)
    hotelId = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    services = models.ManyToManyField(IncludedService)

    def __str__(self):
       return "Hotel di appartenenza --> " + self.hotelId.__str__() + " Room number --> " + str(self.roomNumber)

class Booking(models.Model):
    customerId = models.ForeignKey(User, on_delete=models.CASCADE)
    roomId = models.ForeignKey(Room, on_delete=models.CASCADE)
    checkIn = models.DateField()
    checkOut = models.DateField()

    def __str__(self):
        return self.customerId.__str__() + " " + self.roomId.__str__() + " " + str(self.checkIn) + " " + str(self.checkOut)

