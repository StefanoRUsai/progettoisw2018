from django.db import models
from enum import Enum

class Address(models.Model):
    """classe Address - datatype indirizzo"""

    street = models.CharField(max_length=100)
    houseNumber = models.IntegerField()
    city = models.CharField(max_length=30)
    zipCode = models.CharField(max_length=15)

    # override della funzione Built-in str per la classe
    def __str__(self):
       return str(self.street) + " " + str(self.houseNumber) + " " + str(self.city) + " " + str(self.zipCode)


class Person(models.Model):
    """classe Person, definisce la super classe che rappresenta un'entità di persona"""

    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    birthday = models.DateField()
    cf = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    # override della funzione Built-in str per la classe
    def __str__(self):
        return str(self.name) + " " + str(self.surname) + " " + str(self.birthday) + " " + str(self.cf) + " " + str(self.email) + " " + self.address.__str__()

class Client(Person):
    """classe Client, eredita tutti gli attributi di persona e ha la responsabilità di conoscere
    la propria carta di credito"""

    # override della funzione Built-in str per la classe
    def __str__(self):
        return self.name.__str__()


class CreditCard(models.Model):
    """classe CreditCard, datatype carta di credito"""

    cardNumber = models.CharField(max_length=10)
    expirationYear = models.CharField(max_length=4)
    expirationMonth = models.CharField(max_length=2)
    cvvCode = models.CharField(max_length=3)
    #è l'id del proprietario delle carta di credito, l'entità ha come chiave esterna (nella tecnica ORM) l'id medesimo
    owner = models.ForeignKey(Client, on_delete=models.CASCADE)

    #override della funzione Built-in str per la classe
    def __str__(self):
       return str(self.cardNumber) + " " + str(self.expirationYear) + " " + str(self.expirationMonth) + " " + str(self.cvvCode)


class HotelKeeper(Person):
    """classe Person, rappresenta l'entità Hotel """

    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
       return str(self.name) + " " + str(self.surname)

class RegisteredClient(Client):
    """classe RegisteredClient, rappresenta l'entità del cliente registrato. Eredità tutti gli attributi di person
     e la possibilità di avere una carta di credito da client"""

    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    # override della funzione Built-in str per la classe
    def __str__(self):
       return str(self.username)


class Hotel(models.Model):
    """classe hotel, rappresenta l'entità dell'hotel"""

    name = models.CharField(max_length=30)
    description = models.TextField()
    #chiave esterna del proprietrio dell'hotel, rappresenta l'id del proprietario
    hotelKeeperId = models.ForeignKey(HotelKeeper, on_delete=models.CASCADE)
    #chiave esterna collegata all'indirizzo in cui si trova fisicamente l'hotel, rappresenta l'id dell'indirizzo
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    #tramite il DB si può ottenere l'indirizzo dell'immagine per venire rappresentata sulle view
    photoUrl = models.ImageField(default=None, null=True, upload_to="static/img")

    # override della funzione Built-in str per la classe
    def __str__(self):
       return str(self.name) + " " + self.address.__str__()

class IncludedService(models.Model):
    """classe di enumerazione per rappresentare i servizi della camera"""

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

    # override della funzione Built-in str per la classe
    def __str__(self):
        return self.service.__str__()


class Room(models.Model):
    """classe Room, rappresenta l'entità della stanza"""


    roomNumber = models.IntegerField(default=0)
    capacity = models.IntegerField(default=0)
    price = models.FloatField(default=0.0)
    #rappresenta l'id dell'hotel di appartenenza della stanza, ed è una chiave esterna
    hotelId = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    #rappresenta i servizi della stanza ed è un attributo molti a molti con la metodologia dell'ambiente di lavoro
    services = models.ManyToManyField(IncludedService)

    # override della funzione Built-in str per la classe
    def __str__(self):
       return "Hotel di appartenenza --> " + self.hotelId.__str__() + " Room number --> " + str(self.roomNumber)


class Booking(models.Model):
    """classe Booking, rappresenta l'entità delle prenotazioni"""

    #chiave esterna con l'id del cliente che effettua la prenotazione
    customerId = models.ForeignKey(Client, on_delete=models.CASCADE)
    #chiave esterna con l'id della stanza che viene prenotata
    roomId = models.ForeignKey(Room, on_delete=models.CASCADE)
    checkIn = models.DateField()
    checkOut = models.DateField()


    # override della funzione Built-in str per la classe
    def __str__(self):
        return self.customerId.__str__() + " " + self.roomId.__str__() + " " + str(self.checkIn) + " " + str(self.checkOut)
