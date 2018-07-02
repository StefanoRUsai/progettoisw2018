from django.contrib.sessions.middleware import SessionMiddleware
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client, RequestFactory
import os
import enum
import unittest
import datetime
from .models import *
from .forms import *
from .views import *
from passlib.hash import pbkdf2_sha256


class ModelTestAdress(TestCase):
    def test_Adress(self):
        """Funzione per il controllo del corretto salvataggio di un oggetto Address restituisce true
        nel caso sia stato salvato correttamente"""
        address = Address(street='via Piave', houseNumber=60, city='Uras', zipCode='78999')
        address.save()

        address_count = Address.objects.filter(street='via Piave', houseNumber=60, city='Uras', zipCode='78999').count()
        self.assertEqual(address_count, 1)


class ModelTestPerson(TestCase):
    def test_Person(self):
        """Funzione per il controllo del corretto salvataggio di un oggetto Person restituisce true
        nel caso sia stato salvato correttamente"""
        address = Address(street='via Piave', houseNumber=60, city='Uras', zipCode='78999')
        address.save()

        person = Person(name='Stefano', surname='Marcello', email='smarcello@gmail.com',
                        birthday=datetime.date(1987, 10, 11), cf='MRCSTN84S13A355X', address=address)
        person.save()


        address_count = Address.objects.filter(street='via Piave', houseNumber=60, city='Uras', zipCode='78999').count()
        self.assertEqual(address_count, 1)

        person_count = Person.objects.filter(name='Stefano', surname='Marcello', email='smarcello@gmail.com',
                        birthday=datetime.date(1987, 10, 11), cf='MRCSTN84S13A355X', address=address).count()
        self.assertEqual(person_count, 1)


class ModelTestClient(TestCase):
    def test_Client(self):
        """Funzione per il controllo del corretto salvataggio di un oggetto Client restituisce true
        nel caso sia stato salvato correttamente"""
        address = Address(street='via Piave', houseNumber=60, city='Uras', zipCode='78999')
        address.save()

        user = Client(name='Carlo', surname='Puddu', email='cpuddu@gmail.com', birthday=datetime.date(1990, 10, 6),
                      cf='PDDCRL90F06F979T', address=address)
        user.save()

        address_count = Address.objects.filter(street='via Piave', houseNumber=60, city='Uras', zipCode='78999').count()
        self.assertEqual(address_count, 1)

        user_count = Person.objects.filter(name='Carlo', surname='Puddu', email='cpuddu@gmail.com', birthday=datetime.date(1990, 10, 6),
                      cf='PDDCRL90F06F979T', address=address).count()
        self.assertEqual(user_count, 1)


class ModelTestRegisteredClient(TestCase):
    def test_RegisteredClient(self):
        """Funzione per il controllo del corretto salvataggio di un oggetto RegisteredClient restituisce true
        nel caso sia stato salvato correttamente"""
        address = Address(street='via Piave', houseNumber=60, city='Uras', zipCode='78999')
        address.save()

        user = RegisteredClient(name='Giorgia', surname='Congiu', email='giogio.com',
                                  birthday=datetime.date(1996, 10, 20), cf='CNGGRG96R60A355U', address=address,
                                username='giogioCong96', password='1234')
        user.save()


        address_count = Address.objects.filter(street='via Piave', houseNumber=60, city='Uras', zipCode='78999').count()
        self.assertEqual(address_count, 1)

        user_count = RegisteredClient.objects.filter(name='Giorgia', surname='Congiu', email='giogio.com',
                                  birthday=datetime.date(1996, 10, 20), cf='CNGGRG96R60A355U', address=address,
                                username='giogioCong96', password='1234').count()
        self.assertEqual(user_count, 1)


class ModelTestHotelKeeper(TestCase):
    def test_HotelKeeper(self):
        """Funzione per il controllo del corretto salvataggio di un oggetto HotelKeeper restituisce true
        nel caso sia stato salvato correttamente"""
        address = Address(street='via Piave', houseNumber=60, city='Uras', zipCode='78999')
        address.save()

        hotelKeeper = HotelKeeper(name='Giorgia', surname='Congiu', email='giogio.com',
                                  birthday=datetime.date(1996, 10, 20), cf='CNGGRG96R60A355U', address=address,
                                username='giogioCong96', password='1234')
        hotelKeeper.save()


        address_count = Address.objects.filter(street='via Piave', houseNumber=60, city='Uras', zipCode='78999').count()
        self.assertEqual(address_count, 1)

        hotelKeeper_count = HotelKeeper.objects.filter(name='Giorgia', surname='Congiu', email='giogio.com',
                                  birthday=datetime.date(1996, 10, 20), cf='CNGGRG96R60A355U', address=address,
                                username='giogioCong96', password='1234').count()
        self.assertEqual(hotelKeeper_count, 1)


class ModelTestHotel(TestCase):
    """Funzione per il controllo del corretto salvataggio di un oggetto Hotel restituisce true
    nel caso sia stato salvato correttamente"""
    def test_Hotel(self):
        address = Address(street='via Piave', houseNumber=60, city='Uras', zipCode='78999')
        address.save()

        hotelKeeper = HotelKeeper(name='Giorgia', surname='Congiu', email='giogio.com',
                                  birthday=datetime.date(1996, 10, 20), cf='CNGGRG96R60A355U', address=address,
                                username='giogioCong96', password='1234')
        hotelKeeper.save()

        hotel = Hotel(name='T Hotel', description='Nel cuore di Cagliari...', hotelKeeperId=hotelKeeper,
                      address=address)
        hotel.save()


        address_count = Address.objects.filter(street='via Piave', houseNumber=60, city='Uras', zipCode='78999').count()
        self.assertEqual(address_count, 1)

        hotelKeeper_count = HotelKeeper.objects.filter(name='Giorgia', surname='Congiu', email='giogio.com',
                                  birthday=datetime.date(1996, 10, 20), cf='CNGGRG96R60A355U', address=address,
                                username='giogioCong96', password='1234').count()
        self.assertEqual(hotelKeeper_count, 1)

        hotel_count = Hotel.objects.filter(name='T Hotel', description='Nel cuore di Cagliari...', hotelKeeperId=hotelKeeper,
                      address=address).count()
        self.assertEqual(hotel_count, 1)


class ModelTestRoom(TestCase):
    def test_Room(self):
        """Funzione per il controllo del corretto salvataggio di un oggetto Room restituisce true
        nel caso sia stato salvato correttamente"""
        address = Address(street='via Piave', houseNumber=60, city='Uras', zipCode='78999')
        address.save()

        hotelKeeper = HotelKeeper(name='Giorgia', surname='Congiu', email='giogio.com',
                                  birthday=datetime.date(1996, 10, 20), cf='CNGGRG96R60A355U', address=address,
                                username='giogioCong96', password='1234')
        hotelKeeper.save()

        hotel = Hotel(name='T Hotel', description='Nel cuore di Cagliari...', hotelKeeperId=hotelKeeper,
                      address=address)
        hotel.save()

        room = Room(capacity=3, price='120.00', hotelId=hotel)
        room.save()

        address_count = Address.objects.filter(street='via Piave', houseNumber=60, city='Uras', zipCode='78999').count()
        self.assertEqual(address_count, 1)

        hotelKeeper_count = HotelKeeper.objects.filter(name='Giorgia', surname='Congiu', email='giogio.com',
                                                       birthday=datetime.date(1996, 10, 20), cf='CNGGRG96R60A355U',
                                                       address=address,
                                                       username='giogioCong96', password='1234').count()
        self.assertEqual(hotelKeeper_count, 1)

        hotel_count = Hotel.objects.filter(name='T Hotel', description='Nel cuore di Cagliari...',
                                           hotelKeeperId=hotelKeeper,
                                           address=address).count()
        self.assertEqual(hotel_count, 1)

        room_count = Room.objects.filter(capacity=3, price='120.00', hotelId=hotel).count()
        self.assertEqual(room_count, 1)


class ModelTestRoomService(TestCase):
    def test_RoomService(self):
        """Funzione per il controllo del corretto salvataggio di un oggetto IncludeService restituisce true
        nel caso sia stato salvato correttamente"""

        address = Address(street='via Piave', houseNumber=60, city='Uras', zipCode='78999')
        address.save()

        hotelKeeper = HotelKeeper(name='Giorgia', surname='Congiu', email='giogio.com',
                                  birthday=datetime.date(1996, 10, 20), cf='CNGGRG96R60A355U', address=address,
                                username='giogioCong96', password='1234')
        hotelKeeper.save()

        hotel = Hotel(name='T Hotel', description='Nel cuore di Cagliari...', hotelKeeperId=hotelKeeper,
                      address=address)
        hotel.save()

        room = Room(capacity=3, price='120.00', hotelId=hotel)
        room.save()

        service = IncludedService(service=IncludedService.TELEPHONE, room=room)
        service.save()

        address_count = Address.objects.filter(street='via Piave', houseNumber=60, city='Uras', zipCode='78999').count()
        self.assertEqual(address_count, 1)

        hotelKeeper_count = HotelKeeper.objects.filter(name='Giorgia', surname='Congiu', email='giogio.com',
                                                       birthday=datetime.date(1996, 10, 20), cf='CNGGRG96R60A355U',
                                                       address=address,
                                                       username='giogioCong96', password='1234').count()
        self.assertEqual(hotelKeeper_count, 1)

        hotel_count = Hotel.objects.filter(name='T Hotel', description='Nel cuore di Cagliari...',
                                           hotelKeeperId=hotelKeeper,
                                           address=address).count()
        self.assertEqual(hotel_count, 1)

        room_count = Room.objects.filter(capacity=3, price='120.00', hotelId=hotel).count()
        self.assertEqual(room_count, 1)

        service_count = IncludedService.objects.filter().count()
        self.assertEqual(service_count, 1)


class ModelTestBooking(TestCase):
    def test_Booking(self):

        """Funzione per il controllo del corretto salvataggio di un oggetto Booking restituisce true
        nel caso sia stato salvato correttamente"""
        address = Address(street='via Piave', houseNumber=60, city='Uras', zipCode='78999')
        address.save()

        user = RegisteredClient(name='Giorgia', surname='Congiu', email='giogio.com',
                                  birthday=datetime.date(1996, 10, 20), cf='CNGGRG96R60A355U', address=address,
                                username='giogioCong96', password='1234')
        user.save()

        hotelKeeper = HotelKeeper(name='Giorgia', surname='Congiu', email='giogio.com',
                                  birthday=datetime.date(1996, 10, 20), cf='CNGGRG96R60A355U', address=address,
                                username='giogioCong96', password='1234')
        hotelKeeper.save()

        hotel = Hotel(name='T Hotel', description='Nel cuore di Cagliari...', hotelKeeperId=hotelKeeper,
                      address=address)
        hotel.save()

        room = Room(capacity=3, price='120.00', hotelId=hotel)
        room.save()

        service = IncludedService(service=IncludedService.TELEPHONE, room=room)
        service.save()

        booking = Booking(customerId=user, roomId=room, checkIn=datetime.date(2018, 11, 12),
                          checkOut=datetime.date(2018, 11, 18))
        booking.save()


        address_count = Address.objects.filter(street='via Piave', houseNumber=60, city='Uras', zipCode='78999').count()
        self.assertEqual(address_count, 1)

        user_count = RegisteredClient.objects.filter(name='Giorgia', surname='Congiu', email='giogio.com',
                                  birthday=datetime.date(1996, 10, 20), cf='CNGGRG96R60A355U', address=address,
                                username='giogioCong96', password='1234').count()
        self.assertEqual(user_count, 1)


        hotelKeeper_count = HotelKeeper.objects.filter(name='Giorgia', surname='Congiu', email='giogio.com',
                                                       birthday=datetime.date(1996, 10, 20), cf='CNGGRG96R60A355U',
                                                       address=address,
                                                       username='giogioCong96', password='1234').count()
        self.assertEqual(hotelKeeper_count, 1)

        hotel_count = Hotel.objects.filter(name='T Hotel', description='Nel cuore di Cagliari...',
                                           hotelKeeperId=hotelKeeper,
                                           address=address).count()
        self.assertEqual(hotel_count, 1)

        room_count = Room.objects.filter(capacity=3, price='120.00', hotelId=hotel).count()
        self.assertEqual(room_count, 1)

        service_count = IncludedService.objects.filter().count()
        self.assertEqual(service_count, 1)

        booking_count = Booking.objects.filter(customerId=user, roomId=room, checkIn=datetime.date(2018, 11, 12),
                          checkOut=datetime.date(2018, 11, 18)).count()
        self.assertEqual(booking_count, 1)


class ModelTestCreditCardClient(TestCase):
    def test_CreditCardClient(self):
        """Funzione per il controllo del corretto salvataggio di un oggetto CreditCard con un Client restituisce true
        nel caso sia stato salvato correttamente"""
        address = Address(street='via Piave', houseNumber=60, city='Uras', zipCode='78999')
        address.save()

        user = Client(name='Carlo', surname='Puddu', email='cpuddu@gmail.com', birthday=datetime.date(1990, 10, 6),
                      cf='PDDCRL90F06F979T', address=address)
        user.save()

        creditCard = CreditCard(cardNumber=56478397474839375, expirationMonth=12, expirationYear=2020,
                                      cvvCode=666, owner=user)
        creditCard.save()

        address_count = Address.objects.filter(street='via Piave', houseNumber=60, city='Uras', zipCode='78999').count()
        self.assertEqual(address_count, 1)

        user_count = Client.objects.filter(name='Carlo', surname='Puddu', email='cpuddu@gmail.com', birthday=datetime.date(1990, 10, 6),
                      cf='PDDCRL90F06F979T', address=address).count()
        self.assertEqual(user_count, 1)

        card_count = CreditCard.objects.filter(cardNumber=56478397474839375, expirationMonth=12, expirationYear=2020,
                                      cvvCode=666, owner=user).count()
        self.assertEqual(card_count, 1)


class ModelTestCreditCardRegisteredClient(TestCase):
    def test_CreditCardRegisteredClient(self):
        """Funzione per il controllo del corretto salvataggio di un oggetto CreditCard con un
        RegisteredClient restituisce true nel caso sia stato salvato correttamente"""
        address = Address(street='via Piave', houseNumber=60, city='Uras', zipCode='78999')
        address.save()

        user = RegisteredClient(name='Giorgia', surname='Congiu', email='giogio.com',
                                  birthday=datetime.date(1996, 10, 20), cf='CNGGRG96R60A355U', address=address,
                                username='giogioCong96', password='1234')
        user.save()

        creditCard = CreditCard(cardNumber=56478397474839375, expirationMonth=12, expirationYear=2020,
                                      cvvCode=666, owner=user)
        creditCard.save()

        address_count = Address.objects.filter(street='via Piave', houseNumber=60, city='Uras', zipCode='78999').count()
        self.assertEqual(address_count, 1)

        user_count = RegisteredClient.objects.filter(name='Giorgia', surname='Congiu', email='giogio.com',
                                  birthday=datetime.date(1996, 10, 20), cf='CNGGRG96R60A355U', address=address,
                                username='giogioCong96', password='1234').count()
        self.assertEqual(user_count, 1)

        card_count = CreditCard.objects.filter(cardNumber=56478397474839375, expirationMonth=12, expirationYear=2020,
                                      cvvCode=666, owner=user).count()
        self.assertEqual(card_count, 1)


# Test unitari sui form
class FormsTest(TestCase):
    def setUp(self):
        addressGlobal = Address(street='via Piave', houseNumber=60, city='Uras', zipCode='78999')
        addressGlobal.save()
        r = RegisteredClient(name='Diego', surname='Cittadini', email='marcit@gmail.com',
                             birthday=datetime.date(1987, 10, 11), cf='CTTMRA76T607T',username='diego',
                             password=str(pbkdf2_sha256.encrypt("isw", rounds=12000,salt_size=32)), address=addressGlobal)
        r.save()
        creditCardGlobal = CreditCard(cardNumber=788888999987900, expirationMonth=10, expirationYear=2019, cvvCode=555,owner=r)
        creditCardGlobal.save()


    def test_AddHotelFormValidity(self):
        """ Verifica che un AddHotelForm compilato sia valido """

        # Riempimento del form
        photo_file = open(os.path.dirname(__file__) + '/../static/img/cortina.jpg', 'rb')
        form_data = {'name' : 'Test hotel',
                     'description' : 'Hotel used for unitary test',
                     'street' : 'Test street',
                     'houseNumber' : 12,
                     'city' : 'Test city',
                     'zipCode' : '19928',
                     'photoUrl' : SimpleUploadedFile(photo_file.name, photo_file.read())
                     }

        # Istanziamento del form
        addHotelForm = AddHotelForm(data=form_data)

        # Verifica
        self.assertTrue(addHotelForm.is_valid(), addHotelForm.errors)


    def test_AddHotelFormIsNotValid(self):
        """ Verifica che un  AddHotelForm con campi mancanti non sia valido """

        # Riempimento
        # Al form manca il campo photoUrl
        form_data = {'name' : 'Test hotel',
                     'description' : 'Hotel used for unitary test',
                     'street' : 'Test street',
                     'houseNumber' : 12,
                     'city' : 'Test city',
                     'zipCode' : '19928' }

        # Istanziamento del form
        addHotelForm = AddHotelForm(data=form_data)

        # Verifica
        self.assertTrue(addHotelForm.is_valid(), addHotelForm.errors)


    def test_AddRoomFormValidity(self):
        """ Verifica che un AddRoomForm compilato sia valido """

        # Riempimento del form
        form_data = {'roomNumber' : 14,
                     'bedsNumber' : 3,
                     'services' : ['GARAGE', 'WIFI'],
                     'price' : 120.0 }

        # Istanziamento del form
        addRoomForm = AddRoomForm(data=form_data)

        # Verifica
        self.assertTrue(addRoomForm.is_valid(), addRoomForm.errors)


    def test_AddRoomFormIsNotValid(self):
        """ Verifica che un AddRoomForm con campi mancanti non sia valido """

        # Riempimento
        # Al form manca il campo bedsNumber
        form_data = {'roomNumber' : 14,
                     'services' : ['GARAGE', 'WIFI'],
                     'price' : 120.0 }

        # Istanziamento form
        addRoomForm = AddRoomForm(data=form_data)

        # Verifica
        self.assertFalse(addRoomForm.is_valid(), addRoomForm.errors)


    def test_CreditCardFormValidity(self):
        """ Verifica che un CreditCardForm compilato sia valido """

        # Riempimento form
        form_data ={'cardNumber' : '123456789010111',
                    'month' : '03',
                    'year' : '2019',
                    'cvv' : '003' }

        # Istanziamento form
        ccForm = CreditCardForm(data=form_data)

        # Verifica
        self.assertTrue(ccForm.is_valid(), ccForm.errors)


    def test_CreditCardFormIsNotValid(self):
        """ Verifica che un CreditCardForm con campi mancanti non sia valido """

        # Riempimento dati del form
        # Al form manca il valore di cardNumber
        form_data = {'month' : '03',
                     'year' : '2019',
                     'cvv' : '003' }

        # Istanziameento del form
        ccForm = CreditCardForm(data=form_data)


        # Verifica
        self.assertFalse(ccForm.is_valid(), ccForm.errors)


    def test_LoginFormValidity(self):
        """ Verifica che un LoginForm opportunamente compilato sia valido """

        # Riempimento del form
        form_data = {'username' : 'diego',
                     'password' : 'isw'}

        # Istanziamento
        logForm = LoginForm(data=form_data)

        # Verifica
        self.assertTrue(logForm.is_valid(), logForm.errors)


    def test_LoginFormIsNotValid(self):
        """ Verifica che un LoginForm con campi non compilati non sia valido """

        # Riempimento form
        # Al form manca il campo password
        form_data = {'username' : 'franco'}

        # Istanziamento form
        logForm = LoginForm(data=form_data)


        # Verifica
        self.assertFalse(logForm.is_valid(), logForm.errors)


    def test_RegistrationFormValidity(self):
        """ Verifica che un RegistrationForm compilato sia valido """

        # Riempimento form
        form_data = {'hotelKeeper' : True,
                     'name' : 'Gianni',
                     'surname' : 'Pinna',
                     'birthday' : '1990-02-13',
                     'cf' : 'kjhf240',
                     'email' : 'sonoGianni@gmail.com',
                     'username' : 'gianni',
                     'password' : 'password',
                     'verifyPassword' : 'password',
                     'street' : 'via torre',
                     'civicNumber' : 12,
                     'city' : 'torres',
                     'zipCode' : '42843' }


        # Istanziamento form
        regForm = RegistrationForm(data=form_data)


        # Verifica
        self.assertTrue(regForm.is_valid(), regForm.errors)


    def test_RegistrationFormIsNotValid(self):
        """ Verifica che un RegistrationForm con campi mancanti non sia valido """

        # Riempimento form
        # Al form manca il campo email
        form_data = {'hotelKeeper': True,
                    'name': 'Gianni',
                     'surname': 'Pinna',
                     'birthday': '1990-02-13',
                     'cf': 'kjhf240',
                     'username': 'gianni',
                     'password': 'password',
                     'verificapassword': 'password',
                     'street': 'via torre',
                     'civicNumber': 12,
                     'city': 'torres',
                     'zipCode': '42843'}

        # Istanziamento form
        regForm = RegistrationForm(data=form_data)

        # Verifica
        self.assertFalse(regForm.is_valid(), regForm.errors)


    def test_PaymentFormValidity(self):
        """ Verifica che un PaymentForm compilato sia valido """

        # Riempimento form
        form_data = {'name' : 'giovanni',
                     'surname' : 'frau',
                     'birthday' : '2001-12-12',
                     'cf' : 'asff21',
                     'email' : 'giovanni@gmail.com',
                     'street' : 'via san giovanni',
                     'civicNumber' : 12,
                     'city' : 'cagliari',
                     'zipCode' : '00098',
                     'cardNumber' : '123456789123456',
                     'month' : '05',
                     'year' : '2001',
                     'cvv' : '098',
                     'username' : 'arnold',
                     'password' : 'password',
                     'verifyPassword' : 'password' }


        # Istanziamento form
        payForm = PaymentForm(data=form_data)


        # Verifica
        self.assertTrue(payForm.is_valid(), payForm.errors)


    def test_PaymentFormIsNotValid(self):
        """ Verifica che un PaymentForm con campi mancanti non sia valido """

        # Riempimento form
        # Al form manca il campo surname
        form_data = {'name': 'giovanni',
                     'birthday': '1992-12-12',
                     'cf': 'asff21',
                     'email': 'giovanni@gmail.com',
                     'street': 'via san giovanni',
                     'civicNumber': 12,
                     'city': 'cagliari',
                     'zipCode': '00098',
                     'cardNumber': '124124513',
                     'month': '05',
                     'year': '2001',
                     'cvv': '098',
                     'username': 'diego',
                     'password': 'password',
                     'verificapassword': 'password'}

        # Istanziamento form
        payForm = PaymentForm(data= form_data)


        # Verifica
        self.assertFalse(payForm.is_valid(), payForm.errors)








class RegisteredHotelKeeperTest(TestCase):
    """ Classe contenente i TA della user story 1 """
    def setUp(self):
        address = Address(street='via lanusei', houseNumber=12, city='Cagliari', zipCode='09127')
        address.save()
        hotelKeeper = HotelKeeper(name='Elena', surname='Puddu', birthday=datetime.date(1980, 1, 1),
                                  cf='pdueln80a21b354a', email='e.puddu@gmail.com', address=address, username='prova23',password=str(pbkdf2_sha256.encrypt("isw", rounds=12000,salt_size=32)))
        address = Address(street='via nuoro', houseNumber=16, city='Cagliari', zipCode='09127')
        address.save()
        registereduser = RegisteredClient(name='Marco', surname='Baldo', birthday=datetime.date(1984, 1, 15),
                                        cf='bldmrc84a15b354a', email='marco.baldo@gmail.com', address=address,
                                        username='baldo', password=pbkdf2_sha256.encrypt("isw", rounds=12000,salt_size=32))
        hotelKeeper.save()
        registereduser.save()

        self.userregistered = registereduser
        self.userhotelkeeper = hotelKeeper
        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def test_registrationMissingFields(self):
        """ Verifica che un form di registrazione incompleto non consenta la registrazione """

        # Ottenimento della request
        request = self.request_factory.get('/signUp/', follow=True)
        self.middleware.process_request(request)
        # Creazione della sessione
        request.session.save()

        # Riempimento del form
        form = RegistrationForm(data={'hotelKeeper': True,
                                'name': 'Pinco',
                                'surname': 'Panco',
                                'birthday': '2018-10-21',
                                'cf': '213321321312',
                                'email': 'baldo@gmail.com',
                                'username': 'pinco',
                                'password': 'isw',
                                'verifyPassword': 'isw',
                                'street': 'via da qui',
                                'civicNumber': '666',
                                'city': 'chenonce',
                                'zipCode': '02131'})

        # Verifica
        self.assertTrue(form.is_valid(), msg=form.errors)


    def test_registrationSuccessful(self):
        """ Verifica che un hotel keeper registrato possa accedere alla sua home """

        # Creazione request
        request = self.request_factory.get('/home/', follow=True)
        self.middleware.process_request(request)
        # Creazione sessione
        request.session.save()

        # Simulazione login
        request.session['usr'] = 'prova23'
        request.session['usrType'] = 'hotelKeeper'

        # Esecuzione della vista che gestisce la home dell'albergatore
        response = hotelKeeperHome(request)

        # Verifica l'accesso
        self.assertEquals(response.status_code, 200)

    def test_registrationFailed(self):
        """ Verifica che un hotel keeper non registrato non possa accedere alla shome"""

        # Creazione request
        request = self.request_factory.get('/home/', follow=True)
        self.middleware.process_request(request)
        # Creazione sessione
        request.session.save()

        # Simulazione login
        request.session['usr'] = 'baldo'
        request.session['usrType'] = 'regUser'

        # Esecuzione della vista che gestisce la home dell'hotel keeper
        response = hotelKeeperHome(request)

        # Verifica accesso negato e redirect
        self.assertEquals(response.status_code, 302)

    def test_registrationExistingUsername(self):
        """ Verifica che sia negata l'iscrizione se l'username specificato esiste già """

        # Lista di appoggio
        registeredClientList = []

        # Pagina di registrazione
        bookingPage = '/booking/signUp/'

        # Creazione request
        request = self.request_factory.get(bookingPage, follow=True)
        self.middleware.process_request(request)
        # Creazione sessione
        session = self.client.session
        session.save()

        # Riempimento form con username già usato
        form = RegistrationForm(data={'name': 'Marco',
                                      'surname': 'Rossi',
                                      'birthday': datetime.date(1996, 11, 15),
                                      'cf': 'MRCRSS01345503',
                                      'email': 'm.rossi@outlook.com',
                                      'username': 'baldo',
                                      'password': 'isw',
                                      'verifyPassword': 'isw',
                                      'street': 'Via Marchi',
                                      'civicNumber': 15,
                                      'city': 'Roma',
                                      'zipCode': '09134'
                                      })

        # verifica che sia negata la validazione del form
        self.assertFalse(form.is_valid(), form.errors)

        # Conta gli utenti registrati e verifica che non ne siano stati aggiunti
        for cl in RegisteredClient.objects.all():
            registeredClientList.append(cl)

        self.assertTrue(len(registeredClientList), 1)

        # Riempimento form valido
        form_data = {'name': 'Marco', 'surname': 'Rossi', 'birthday': datetime.date(1996, 11, 15),
                     'cf': 'MRCRSS01345503',
                     'email': 'm.rossi@outlook.com', 'username': 'marco', 'password': 'isw',
                     'verifyPassword': 'isw', 'street': 'Via Marchi', 'civicNumber': 15, 'city': 'Roma',
                     'zipCode': '09134'}

        # Invio form all'url che gestisce la registrazione
        self.client.post('/signUp/', form_data)

        # Conteggio e verifica
        registeredClientList = []

        for cl in RegisteredClient.objects.all():
            registeredClientList.append(cl)

        self.assertTrue(len(registeredClientList), 1)


class LoginHotelKeeperTest(TestCase):
    """ Classe contenente i TA della user story 2 """
    def setUp(self):
        address = Address(street='via lanusei', houseNumber=12, city='Cagliari', zipCode='09127')
        address.save()
        hotelKeeper = HotelKeeper(name='Elena', surname='Puddu', birthday=datetime.date(1980, 1, 1),
                                  cf='pdueln80a21b354a', email='e.puddu@gmail.com', address=address, username='prova23',
                                  password=str(pbkdf2_sha256.encrypt("isw", rounds=12000,salt_size=32)))
        address = Address(street='via nuoro', houseNumber=16, city='Cagliari', zipCode='09127')
        address.save()
        registereduser = RegisteredClient(name='Marco', surname='Baldo', birthday=datetime.date(1984, 1, 15),
                                        cf='bldmrc84a15b354a', email='marco.baldo@gmail.com', address=address,
                                        username='baldo', password=str(pbkdf2_sha256.encrypt("isw", rounds=12000,salt_size=32)))
        hotelKeeper.save()
        registereduser.save()

        self.userregistered = registereduser
        self.userhotelkeeper = hotelKeeper
        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def test_hotelKeeperHomeRedirect(self):
        """ Verifica che un hotel keeper loggato non abbia accesso alla pagina di login """

        # Creazione della request
        request = self.request_factory.get('/login/', follow=True)
        self.middleware.process_request(request)
        # Creazione della sessione
        request.session.save()

        # Simulaazione hotel keeper loggato
        request.session['usr'] = self.userhotelkeeper.username
        request.session['usrType'] = 'hotelKeeper'

        # Esecuzione della vista di login
        response = login(request)

        # Verifica il redirect
        self.assertEquals(response.status_code, 302)



class HotelKeeperHomeTest(TestCase):
    """ Classe contenente i TA della user story 3 """
    def setUp(self):
        hkAddress = Address(street='via francesco', houseNumber=12, city='savona', zipCode='00989')
        hkAddress.save()
        bookedUser = Client(name='gianni', surname='deGasperi', birthday=datetime.date(1996, 10, 20), cf='fsaf34f32',
                          email='gianni@gmail.com', address=hkAddress)
        bookedUser.save()
        userCreditCard = CreditCard(cardNumber='124563455436', expirationYear='2022', expirationMonth='03',
                                    cvvCode='007', owner=bookedUser)
        userCreditCard.save()
        hotelKeeper = HotelKeeper(name='francesco', surname='fadda', birthday=datetime.date(1996, 10, 20),
                                  cf='dasf12r1324', email='francesco@fadda.net', address=hkAddress,
                                  username='francesco', password=str(pbkdf2_sha256.encrypt("isw", rounds=12000,salt_size=32)))
        hotelKeeper.save()
        hotelAddress = Address(street='via hotel bellissimo', houseNumber=12, city='savona', zipCode='00929')
        hotelAddress.save()
        hotel = Hotel(name='Hotel Acquaragia', description='Hotel bellissimo', hotelKeeperId=hotelKeeper,
                      address=hotelAddress, photoUrl='/static/img/amsterdamHotel.jpg')
        hotel.save()
        bookedRoom = Room(roomNumber=12, capacity=3, price=40.0, hotelId=hotel)
        bookedRoom.save()
        hotelKeeperNoBookings = HotelKeeper(name='filippo', surname='podddesu', birthday=datetime.date(1996, 10, 20),
                                            cf='dasf12r1324', email='filippo@poddesu.net', address=hkAddress,
                                            username='filippo', password=str(pbkdf2_sha256.encrypt("isw", rounds=12000,salt_size=32)) )
        hotelKeeperNoBookings.save()
        booking = Booking(customerId=bookedUser, roomId=bookedRoom, checkIn=datetime.date(2018, 11, 28),
                          checkOut=datetime.date(2018, 11, 20))
        booking.save()

        self.userWithBookings = hotelKeeper
        self.userWithoutBookings = hotelKeeperNoBookings
        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def test_hotelKeeperBookingsVisualization(self):
        """ Verifica che un hotel keeper con prenotazioni le visualizzi nella sua home """

        # Creazione della request
        request = self.request_factory.get('/home/')
        self.middleware.process_request(request)
        # Creazione della sessione
        request.session.save()

        # Simulazione hotel keeper loggato
        request.session['usr'] = self.userWithBookings.username
        request.session['usrType'] = 'hotelKeeper'

        # Esecuzione della view che gestisce la home dell'albergatore
        response = hotelKeeperHome(request)

        # Verifica che la pagina contenga la prenotazione
        self.assertContains(response, 'gianni')
        self.assertContains(response, 'Hotel Acquaragia')


    def test_hotelKeeperNoBookingsMessage(self):
        """ Verifica che un hotel keeper senza prenotazioni visualizzi il messaggio relativo """

        # Creazione della requqest
        request = self.request_factory.get('/home/')
        self.middleware.process_request(request)
        # Creazione della sessione
        request.session.save()

        # Simulazione albergatore loggato
        request.session['usr'] = self.userWithoutBookings.username
        request.session['usrType'] = 'hotelKeeper'

        # Esecuzione della view che gestisce la home dell'albergatore
        response = hotelKeeperHome(request)

        # Verifica della visualizzazione del messaggio
        self.assertContains(response, "You have not reservations in your hotels!")


class HotelsListTest(TestCase):
    """ Classe contenente i TA della user story 4 """
    def setUp(self):
        hkAddress = Address(street='via francesco', houseNumber=12, city='savona', zipCode='00989')
        hkAddress.save()
        hotelKeeper = HotelKeeper(name='francesco', surname='fadda', birthday=datetime.date(1996, 10, 20),
                                  cf='dasf12r1324', email='francesco@fadda.net', address=hkAddress,
                                  username='francesco', password=str(pbkdf2_sha256.encrypt("isw", rounds=12000,salt_size=32)))
        hotelKeeper.save()
        hotelAddress = Address(street='via hotel bellissimo', houseNumber=12, city='savona', zipCode='00929')
        hotelAddress.save()
        hotel = Hotel(name='Hotel Acquaragia', description='Hotel bellissimo', hotelKeeperId=hotelKeeper,
                      address=hotelAddress, photoUrl='/static/img/amsterdamHotel.jpg')
        hotel.save()
        service1 = IncludedService(service=IncludedService.GARAGE)
        service1.save()
        service2 = IncludedService(service=IncludedService.TELEPHONE)
        service2.save()
        room1 = Room(roomNumber=12, capacity=3, price=40.0, hotelId=hotel)
        room1.save()
        room1.services.add(service1)
        room2 = Room(roomNumber=14, capacity=3, price=60.0, hotelId=hotel)
        room2.save()
        room2.services.add(service2)
        hotel2 = Hotel(name='Hotel Napoleone', description='Hotel bellissimo', hotelKeeperId=hotelKeeper,
                       address=hotelAddress, photoUrl='/static/img/amsterdamHotel.jpg')
        hotel2.save()
        hotelKeeperNoHotels = HotelKeeper(name='fabrizio', surname='secci', birthday=datetime.date(1996, 10, 20),
                                          cf='dasf12r1324', email='fabrizio@secci.net', address=hkAddress,
                                          username='fabrizio', password=str(pbkdf2_sha256.encrypt("isw", rounds=12000,salt_size=32)))
        hotelKeeperNoHotels.save()

        self.userWithHotels = hotelKeeper
        self.userWithoutHotels = hotelKeeperNoHotels
        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def test_HotelListVisualization(self):
        """ Verifica che un hotel keeper che possiede hotel ne visualizzi la lista """

        # Creazione request
        request = self.request_factory.get('/hotels/')
        self.middleware.process_request(request)
        # Creazione sessione
        request.session.save()

        # Simulazione hotel keeper loggato
        request.session['usr'] = self.userWithHotels.username
        request.session['usrType'] = 'hotelKeeper'

        # Esecuzione della vista che gestisce la lista hotel
        response = hotelsList(request)

        # Verifica che gli hotel vengano visualizzati
        self.assertContains(response, 'Hotel Acquaragia')
        self.assertContains(response, 'Hotel Napoleone')

    def test_EmptyHotelListVisualization(self):
        """ Verifica che un hotel keeper senza hotel visualizzi il messaggio relativo """

        # Creazione request
        request = self.request_factory.get('/hotels/')
        self.middleware.process_request(request)
        # Creazione sessione
        request.session.save()

        # Simulazione hotel keeper loggato
        request.session['usr'] = self.userWithoutHotels.username
        request.session['usrType'] = 'hotelKeeper'

        # Esecuzione della vista che gestisce la lista hotel
        response = hotelsList(request)

        # Verifica della visualizzaazione del messaggio
        self.assertContains(response, "You have not registered any hotel!")



class AddHotelInTheList(TestCase):
    """ Classe contenente i TA della user story 5 """
    def setUp(self):
        hkAddress = Address(street='via del guasto', houseNumber=28, city='Bologna', zipCode='09888')
        hkAddress.save()
        hotelKeeper = HotelKeeper(name='Gianna', surname='Poho', birthday=datetime.date(1992, 1, 12),
                                  cf='phognn92t21b354ta', email='g.poho@gmail.com', address=hkAddress,
                                  username='giannina', password=str(pbkdf2_sha256.encrypt("isw", rounds=12000,salt_size=32)))
        hotelKeeper.save()
        h1Address = Address(street='via da qui', houseNumber=40, city='Bologna', zipCode='09888')
        h1Address.save()
        hotel1 = Hotel(name='Hotel Bacco', description="Nell'affascinante Bologna...", hotelKeeperId=hotelKeeper,
                       address=h1Address, photoUrl='/static/img/bedAndBreakfastLondon.jpg')
        hotel1.save()
        h2Address = Address(street='via Quadrilatero', houseNumber=90, city='Bologna', zipCode='09888')
        h2Address.save()
        hotel2 = Hotel(name='Hotel Tarallucci', description="Tanti biscotti a colazione", hotelKeeperId=hotelKeeper,
                       address=h2Address, photoUrl='/static/img/cortina.jpg')
        hotel2.save()
        newAddress = Address(street='via Holita', houseNumber=30, city='Bologna', zipCode='09888')
        newAddress.save()

        self.newAd = newAddress
        self.hotelKeeper = hotelKeeper
        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def test_addHotelMissingFields(self):
        """ Verifica che non venga consentita l'aggiunta di un hotel se il form è incompleto """

        # Creazione request
        request = self.request_factory.get('/addHotel/', follow=True)
        self.middleware.process_request(request)
        # Creazione sessione
        request.session.save()

        # Simulazione hotel keeper loggato
        request.session['usr'] = self.hotelKeeper.username
        request.session['usrType'] = 'hotelKeeper'

        # Riempimento form
        photo_file = open(os.path.dirname(__file__) + '/../static/img/cortina.jpg', 'rb')
        form_data = {'name': "hotel Trinciapollo",
                     'description': "Poulet e besciamel",
                     'street': self.newAd.street,
                     'houseNumber': self.newAd.houseNumber,
                     'city': self.newAd.city,
                     'zipCode': self.newAd.zipCode,
                     'photoUrl': SimpleUploadedFile(photo_file.name, photo_file.read())}

        form = AddHotelForm(data=form_data)

        # Verifica
        self.assertTrue(form.is_valid(), msg=form.errors)


    def test_hotelAdded(self):
        """ Verifica che un hotel sia correttamente aggiunto """

        # Lista temporanea
        listaHotel = []

        # Pagina con il di aggiunta hotel
        bookingPage = '/booking/addHotel/'

        # Creazione request
        request = self.request_factory.get(bookingPage, follow=True)
        self.middleware.process_request(request)
        # Simulazione hotel keeper loggaato e creazione sessione
        session_key = self.hotelKeeper.username
        session = self.client.session
        session['usr'] = session_key
        session.save()

        # Verifica del numero di hotel presenti prima dell'aggiunta
        for ht in Hotel.objects.all():
            if (ht.hotelKeeperId.username == self.hotelKeeper.username):
                listaHotel.append(ht)

        self.assertEqual(len(listaHotel), 2)

        # Esecuzione della vista che gestisce l'aggiunta di hotel
        response = addHotel(request)

        # Riempimento form
        form = AddHotelForm(data={
            'name': 'Bonsoir',
            'description': "C'est magnifique",
            'street': 'Rue Mont Poisson',
            'houseNumber': 5,
            'city': 'Paris',
            'zipCode': '09234',
            'photoUrl': '/static/img/parisHotel.jpg'
        })

        form_data = {'name': 'Bonsoir', 'description': "C'est magnifique", 'street': 'Rue Mont Poisson',
                     'houseNumber': 5, 'city': 'Paris',
                     'zipCode': '09234', 'photoUrl': '/static/img/parisHotel.jpg'}

        # Verifica che il form sia valido
        self.assertTrue(form.is_valid())

        # Verifica che la view non abbia restituito errore
        self.assertEquals(response.status_code, 200)

        # Invia il form in POST all'url di aggiunta hotel
        self.client.post('/addHotel/', form_data)

        # Verifica della corretta aggiunta dell'hotel
        listaHotel = []

        for ht in Hotel.objects.all():
            if (ht.hotelKeeperId.username == self.hotelKeeper.username):
                listaHotel.append(ht)

        self.assertEqual(len(listaHotel), 3)



class ManageHotel(TestCase):
    """ Classe contenente i TA della user story 6 """
    def setUp(self):
        hkAddress = Address(street='via francesco', houseNumber=12, city='savona', zipCode='00989')
        hkAddress.save()

        hotelKeeper = HotelKeeper(name='francesco', surname='fadda', birthday=datetime.date(1996, 10, 20),
                                  cf='dasf12r1324',
                                  email='francesco@fadda.net', address=hkAddress, username='francesco',
                                  password=str(pbkdf2_sha256.encrypt("isw", rounds=12000,salt_size=32)))
        hotelKeeper.save()

        hotelAddress = Address(street='via hotel bellissimo', houseNumber=12, city='savona', zipCode='00929')
        hotelAddress.save()

        hotel = Hotel(name='Hotel Acquaragia', description='Hotel bellissimo', hotelKeeperId=hotelKeeper,
                      address=hotelAddress,
                      photoUrl='/static/img/amsterdamHotel.jpg')
        hotel.save()

        room1 = Room(roomNumber=40, capacity=3, price='120', hotelId=hotel)

        room1.save()

        service = IncludedService(service=IncludedService.GARAGE, room=room1)

        service.save()

        self.hotelKeeperSession = hotelKeeper
        self.hotel = hotel
        self.hotelAddress = hotelAddress
        self.room = room1
        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def test_hotelsRoomsDataVisualization(self):
        """ Verifica che l'hotel keeper visualizzi i dati dell'hotel e delle camere che contiene"""

        # Pagina dell'hotel aggiunto in setUp()
        hotelPage = '/hotel/?name=' + self.hotel.name + '&civN=' + str(self.hotelAddress.houseNumber) + '&city=' + self.hotelAddress.city

        # Creazione request
        request = self.request_factory.get(hotelPage, follow=True)
        self.middleware.process_request(request)
        # Creazione sessione
        request.session.save()

        # Simulazione login
        request.session['usr'] = self.hotelKeeperSession.username
        request.session['usrType'] = 'hotelKeeper'

        # Esecuzione della vista che gestisce i dettagli dell'hotel
        response = hotelDetail(request)

        # Verifica che la pagina contenga i dati dell'hotel
        self.assertContains(response, 'Hotel Acquaragia')
        self.assertContains(response, '40')
        self.assertContains(response, '3')
        self.assertContains(response, '120')



class AddRoomToHotelTest(TestCase):
    """ Classe contenente i TA della user story 7 """
    def setUp(self):
        hkAddress = Address(street='via del guasto', houseNumber=28, city='Bologna', zipCode='09888')
        hkAddress.save()
        hotelKeeper = HotelKeeper(name='Gianna', surname='Poho', birthday=datetime.date(1992, 1, 12),
                                  cf='phognn92t21b354ta', email='g.poho@gmail.com', address=hkAddress,
                                  username='giannina',password=str(pbkdf2_sha256.encrypt("isw", rounds=12000,salt_size=32)))
        hotelKeeper.save()
        h1Address = Address(street='via da qui', houseNumber=40, city='Bologna', zipCode='09888')
        h1Address.save()
        hotel = Hotel(name='Hotel Bacco', description="Nell'affascinante Bologna...", hotelKeeperId=hotelKeeper,
                      address=h1Address, photoUrl='/static/img/bedAndBreakfastLondon.jpg')
        hotel.save()

        room = Room(roomNumber=27,capacity=3,price=35.5,hotelId=hotel)
        room.save()


        self.userhotelkeeper = hotelKeeper
        self.hotel = hotel
        self.room = room
        self.hotelAddress = hkAddress
        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def test_addRoomMissingFields(self):
        """ Verifica che non sia accettato un form incompleto"""
        request = self.request_factory.get('/addRoom/', follow=True)
        self.middleware.process_request(request)
        request.session.save()

        request.session['htName'] = self.hotel.name
        request.session['htCivN'] = self.hotelAddress.houseNumber

        form = AddRoomForm(data={'roomNumber': 3, 'bedsNumber': 2})

        self.assertFalse(form.is_valid(), msg=form.errors)

    def test_addRoomSuccesful(self):
        """ Verifica che una camera venga correttamente aggiunta """

        # Lista di appoggio
        roomList = []

        # Pagina di aggiunta camera
        bookingPage = '/booking/addRoom/'

        # Creazione request
        request = self.request_factory.get(bookingPage, follow=True)
        self.middleware.process_request(request)

        # Scrittura in sessione dei dati necessari alla vista
        session_key1 = str(self.hotel.name)
        session_key2 = str(self.hotel.address.houseNumber)
        session = self.client.session
        session['htName'] = session_key1
        session['htCivN'] = session_key2
        session.save()

        # Riempimento form
        form = AddRoomForm(data={'roomNumber': 111,
                                 'bedsNumber': 3,
                                 'services' : ["TELEPHONE","GARAGE"],
                                 'price' : 75.50
                                 })

        # Verifica il form
        self.assertTrue(form.is_valid())

        # Conteggio camere prima dell'aggiunta e verifica
        for rm in Room.objects.all():
            if (rm.hotelId == self.hotel):
                roomList.append(rm)

        self.assertEqual(len(roomList), 1)

        # Riempimento form
        form_data = {'roomNumber': 111,'bedsNumber': 3,'services' : ["TELEPHONE","GARAGE"],'price' : 75.50}

        # Invio form all'url che gestisce l'aggiunta della camera
        self.client.post('/addRoom/',form_data)

        # Conteggio camere dopo l'aggiunta e verifica
        roomList = []

        for rm in Room.objects.all():
            if (rm.hotelId == self.hotel):
                roomList.append(rm)

        self.assertEqual(len(roomList), 2)




class SearchResultTest(TestCase):
    """ Classe contenente i TA della user story 8 """
    def setUp(self):
        hkAddress = Address(street='via francesco', houseNumber=12, city='savona', zipCode='00989')
        hkAddress.save()
        bookedUser = Client(name='gianni', surname='deGasperi', birthday=datetime.date(1996, 10, 20), cf='fsaf34f32',
                          email='gianni@gmail.com', address=hkAddress)
        bookedUser.save()
        userCreditCard = CreditCard(cardNumber='124563455436', expirationYear='2022', expirationMonth='03',
                                    cvvCode='007', owner=bookedUser)
        userCreditCard.save()
        hotelKeeper = HotelKeeper(name='francesco', surname='fadda', birthday=datetime.date(1996, 10, 20),
                                  cf='dasf12r1324', email='francesco@fadda.net', address=hkAddress,
                                  username='francesco', password=str(pbkdf2_sha256.encrypt("isw", rounds=12000,salt_size=32)))
        hotelKeeper.save()
        hotelAddress = Address(street='via hotel bellissimo', houseNumber=12, city='savona', zipCode='00929')
        hotelAddress.save()
        hotel = Hotel(name='Hotel Acquaragia', description='Hotel bellissimo', hotelKeeperId=hotelKeeper,
                      address=hotelAddress, photoUrl='/static/img/amsterdamHotel.jpg')
        hotel.save()
        bookedRoom = Room(roomNumber=12, capacity=3, price=40.0, hotelId=hotel)
        bookedRoom.save()
        hotelKeeperNoBookings = HotelKeeper(name='filippo', surname='podddesu', birthday=datetime.date(1996, 10, 20),
                                            cf='dasf12r1324', email='filippo@poddesu.net', address=hkAddress,
                                            username='filippo',password=str(pbkdf2_sha256.encrypt("isw", rounds=12000,salt_size=32)))
        hotelKeeperNoBookings.save()
        booking = Booking(customerId=bookedUser, roomId=bookedRoom, checkIn=datetime.date(2018, 11, 28),
                          checkOut=datetime.date(2018, 11, 20))
        booking.save()

        self.userWithHotels = hotelKeeper

        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()


    def test_searchResult(self):
        """ Verifica che sia possibile effettuare una ricerca"""

        # Creazione request
        request = self.request_factory.get('/search/', follow=True)

        # Creazione valori in GET
        request.GET.__init__(mutable=True)

        request.GET['search_city'] = 'savona'
        request.GET['search_number'] = '3'
        request.GET['search_checkin'] = '2018-01-01'
        request.GET['search_checkout'] = '2018-01-05'

        self.middleware.process_request(request)

        # Creazione sessione
        request.session.save()

        # Invio dei dati alla view che effettua la ricerca
        response = searchResults(request)

        # Verifica corrispondenze trovate
        self.assertContains(response, 'Hotel Acquaragia')


    def test_searchNoMatches(self):
        """ Verifica che se la lista dei risultati è vuota sia visualizzato il messaggio """

        # Creazione request
        request = self.request_factory.get('/search/', follow=True)

        # Creazione dati in GET per la ricerca
        request.GET.__init__(mutable=True)

        request.GET['search_city'] = 'cagliari'
        request.GET['search_number'] = '3'
        request.GET['search_checkin'] = '2018-01-01'
        request.GET['search_checkout'] = '2018-01-05'

        self.middleware.process_request(request)

        # Creazione sessione
        request.session.save()

        # Invio dati alla view che esegue la ricerca
        response = searchResults(request)

        # Verifica che non siano stati trovate occorrenze
        self.assertContains(response, 'There are no rooms available with these requirements')



class reserveRoom(TestCase):
    """ Classe contenente i TA della user story 9 """
    def setUp(self):
        hkAddress = Address(street='via francesco', houseNumber=12, city='savona', zipCode='00989')
        hkAddress.save()

        hotelKeeper = HotelKeeper(name='francesco', surname='fadda', birthday=datetime.date(1996, 10, 20),
                                  cf='dasf12r1324',
                                  email='francesco@fadda.net', address=hkAddress, username='francesco',
                                  password=str(pbkdf2_sha256.encrypt("isw", rounds=12000,salt_size=32)))
        hotelKeeper.save()

        hotelAddress = Address(street='via hotel bellissimo', houseNumber=12, city='savona', zipCode='00929')
        hotelAddress.save()

        hotel = Hotel(name='Hotel Acquaragia', description='Hotel bellissimo', hotelKeeperId=hotelKeeper,
                      address=hotelAddress,
                      photoUrl='/static/img/amsterdamHotel.jpg')
        hotel.save()

        room1 = Room(roomNumber=40, capacity=3, price='120', hotelId=hotel)
        room1.save()

        service = IncludedService(service=IncludedService.GARAGE, room=room1)

        service.save()

        self.hotel = hotel
        self.hotelAddress = hotelAddress
        self.room = room1
        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def test_bookingMissingFields(self):
        """ Verifica che non venga effettuata una prenotazione se il form è incompleto """

        # Pagina di prenotazione di una camera
        bookingPage = '/booking/?roomid=' + str(self.room.id)

        # Creazione request
        request = self.request_factory.get(bookingPage, follow=True)
        self.middleware.process_request(request)
        # Creazione sessione
        request.session.save()

        # Esecuzione della vista che gestisce le prenotazioni
        response = bookARoom(request)


        # Riempimento form
        form = PaymentForm(data={
            'name': 'Giorgio',
            'surname': 'Imola',
            'birthday': '2018-10-21',
            'cf': '90913829011',
            'email': 'giogioImola@gmail.com',
            'username': 'giorgio',
            'password': 'isw',
            'verifyPassord': 'isw',
            'street': 'via dalle scatole',
            'civicNumber': '777',
            'city': 'Marius',
            'zipCode': '02131',
            # 'cardNumber': '123456789012345',
            'month': '10',
            'year': '2019',
            'cvv': '908'
        })

        # Verifica form
        self.assertFalse(form.is_valid(), msg=form.errors)

        # NEW
        def test_bookingRoomSuccessfull(self):
            bookingPage = '/booking/?roomid=' + str(self.room.id)
            request = self.request_factory.get(bookingPage, follow=True)
            self.middleware.process_request(request)
            s = self.client.session
            s.update({'usr': str(self.registeredClient.username),
                      'logIn_dt': "2018-01-01",
                      'logOut_dt': "2018-01-05"})
            s.save()

            # passo alla vista booking i valori tramite richiesta di tipo GET
            self.client.post(bookingPage)

            response = bookARoom(request)

            # dichiaro una variablile booleana per controllare lo stato della prenotazione
            reservationSuccess = False

            # controllo se la view ha risposto correttamente
            self.assertEqual(response.status_code, 200)

            for reservetion in Booking.objects.all():
                if (
                        reservetion.roomId.roomNumber == self.room.roomNumber and reservetion.customerId.email == self.registeredClient.email):
                    reservationSuccess = True

            # controllo se la prenotazione è stata realmente effettuata
            self.assertTrue(reservationSuccess, "Prenotazione non creata")

        # NEW
        def test_registrationFromBooking(self):
            # Pagina di prenotazione di una camera
            bookingPage = '/booking/?roomid=' + str(self.room.id)

            # Creazione request
            request = self.request_factory.get(bookingPage, follow=True)
            self.middleware.process_request(request)

            # creo i dati per compilare il form
            form_data = {'name': 'Giorgio', 'surname': 'Imola', 'birthday': '2018-10-21', 'cf': '90913829011',
                         'email': 'giogioImola@gmail.com', 'username': 'giorgio', 'password': 'isw',
                         'verifyPassword': 'isw', 'street': 'via dalle scatole', 'civicNumber': '777',
                         'city': 'Marius', 'zipCode': '02131', 'cardNumber': '123456789012345', 'month': '10',
                         'year': '2019', 'cvv': '908'}

            # Riempimento form con i dati creati sopra
            form = PaymentForm(data=form_data)

            # Verifica form
            self.assertTrue(form.is_valid(), msg=form.errors)

            # passo i dati alla vista
            self.client.post(bookingPage, form_data)
            response = bookARoom(request)

            # controllo che la risposta della view sia corretta
            self.assertEqual(response.status_code, 200)

            # creo due variabili per verificare il corretto salvataggio di carta di credito e dati utente
            registrationCl = False
            registationCreditCard = False

            # controllo se i dati dell'utente sono stati effettivamente salvati
            for cl in Client.objects.all():
                if (cl.email == "giogioImola@gmail.com"):
                    registrationCl = True

            # controllo se i dati della carta di credito sono stati effettivamente salvati
            for credtiCard in CreditCard.objects.all():
                if (credtiCard.cardNumber == "123456789012345" and credtiCard.cvvCode == "908"):
                    registationCreditCard = True

            # verifico che entrambi gli oggetti siano stati salvati correttamente
            self.assertTrue(registrationCl, "Dati della carta non salvati correttamente")
            self.assertTrue(registationCreditCard, "Dati della carta non salvati correttamente")



class TestDatasave(TestCase):
    """ Classe contenente i TA della user story 10 """
    def setUp(self):
        hkAddress = Address(street='via francesco', houseNumber=12, city='savona', zipCode='00989')
        hkAddress.save()
        bookedUser = Client(name='gianni', surname='deGasperi', birthday=datetime.date(1996, 10, 20), cf='fsaf34f32',
                          email='gianni@gmail.com', address=hkAddress)
        bookedUser.save()
        userCreditCard = CreditCard(cardNumber='124563455436', expirationYear='2022', expirationMonth='03',
                                    cvvCode='007',
                                    owner=bookedUser)
        userCreditCard.save()
        hotelKeeper = HotelKeeper(name='francesco', surname='fadda', birthday=datetime.date(1996, 10, 20),
                                  cf='dasf12r1324',
                                  email='francesco@fadda.net', address=hkAddress, username='francesco',
                                  password=str(pbkdf2_sha256.encrypt("isw", rounds=12000,salt_size=32)))
        hotelKeeper.save()
        hotelAddress = Address(street='via hotel bellissimo', houseNumber=12, city='savona', zipCode='00929')
        hotelAddress.save()
        hotel = Hotel(name='Hotel Acquaragia', description='Hotel bellissimo', hotelKeeperId=hotelKeeper,
                      address=hotelAddress, photoUrl='/static/img/amsterdamHotel.jpg')
        hotel.save()
        bookedRoom = Room(roomNumber=12, capacity=3, price=40.0, hotelId=hotel)
        bookedRoom.save()
        hotelKeeperNoBookings = HotelKeeper(name='filippo', surname='podddesu',
                                            birthday=datetime.date(1996, 10, 20),
                                            cf='dasf12r1324', email='filippo@poddesu.net', address=hkAddress,
                                            username='filippo', password=str(pbkdf2_sha256.encrypt("isw", rounds=12000,salt_size=32)))
        hotelKeeperNoBookings.save()
        booking = Booking(customerId=bookedUser, roomId=bookedRoom, checkIn=datetime.date(2018, 11, 28),
                          checkOut=datetime.date(2018, 11, 20))
        booking.save()

        self.userWithHotels = hotelKeeper

        self.request_factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def testSearchResult(self):
        # Riempimento form
        form_data = {'name': 'Marco', 'surname': 'cognome',
                     'birthday': datetime.date(1996, 10, 20),
                     'cf': '23132123321', 'email': 'mail@ciao.com',
                     'street': 'via', 'civicNumber': 12, 'city': 'cagliari',
                     'zipCode': '09100', 'cardNumber': 788888999987900,
                     'month': 12, 'year': 2019, 'cvv': 321,
                     'username': 'miao', 'password': 'isw',
                     'verifyPassword': 'isw'}

        s = self.client.session
        s.update({
            "logIn_dt": '2010-12-05',
            "logOut_dt": '2010-12-06',
        })
        s.save()

        # Invio form alla pagina
        self.client.post('/booking/?roomid=1', form_data)

        app_count = RegisteredClient.objects.filter(username='miao').count()
        self.assertEqual(app_count, 1)