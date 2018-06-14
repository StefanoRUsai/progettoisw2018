from django.db import models

# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    date = models.DateField()
    cf = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)

class User(Person):
    #to do carta di credito

