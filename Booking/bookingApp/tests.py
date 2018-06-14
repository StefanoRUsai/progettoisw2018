from django.test import TestCase

from enum import Enum

import unittest
from .models import *

class ModelTest(TestCase):
    def setUp(self):
        person = Person(name = 'Stefano', surname = 'Usai', email = 'susai@gmail.com', birthday = '30/10/1984', cf = 'SUASFN84R30B354E')
        person.save()
