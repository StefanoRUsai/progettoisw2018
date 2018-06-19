from django.db import models


class CreditCard(models.Model):
    cardNumber = models.IntegerField()
    expirationYear = models.IntegerField()
    expirationMonth = models.IntegerField()
    cvvCode = models.IntegerField()


class Address(models.Model):
    street = models.CharField(max_length=100)
    houseNumber = models.IntegerField()
    city = models.CharField(max_length=30)
    zipCode = models.CharField(max_length=15)


class Person(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    date = models.DateField()
    cf = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    address = models.ForeignKey(Address,on_delete=models.CASCADE)


class User(Person):
    creditCard = models.ForeignKey(CreditCard, on_delete=models.CASCADE, null=True)


class HotelKeeper(Person):
    userName = models.CharField(max_length=50)
    password = models.CharField(max_length=50)


class RegisteredUser(User):
    userName = models.CharField(max_length=50)
    password = models.CharField(max_length=50)


class Hotel(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    hotelKeeperId = models.ForeignKey(HotelKeeper, on_delete=models.CASCADE)
    address = models.ForeignKey(Address,on_delete=models.CASCADE)
    photoUrl = models.ImageField(default=None, null=True)


class Room(models.Model):
    capacity = models.IntegerField(default=0)
    price = models.FloatField(default=0.0)
    SERVICES = ( (0, "Minibar"), (1, "Telephone"), (2, "Breakfast") )
    service = models.IntegerField(max_length=1, choices=SERVICES, default=None)
    hotelId = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    photoUrl = models.ImageField(default=None, null=True)


class Booking(models.Model):
    customerId = models.ForeignKey(User, on_delete=models.CASCADE)
    roomId = models.ForeignKey(Room, on_delete=models.CASCADE)
    checkIn = models.DateField()
    checkOut = models.DateField()


