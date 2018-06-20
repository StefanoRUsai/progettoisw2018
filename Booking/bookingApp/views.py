from django.shortcuts import render, redirect
from .forms import AddHotelForm,AddRoomForm,formLogin
from .models import Hotel,Address,Room,IncludedService,RegisteredUser


def login(request):
    if(request.method == 'POST'):
        form = formLogin(request.POST)
        if(form.is_valid()):
            #Setto in sessione le variabili relative all'utente loggato tranne la password
            userN = form.cleaned_data['username']
            passW = form.cleaned_data['password']

            for ut in RegisteredUser.objects.all():
                if(ut.username == userN and ut.password == passW):
                    request.session['usr'] = form.cleaned_data['username']
                    return redirect('/homeRegistered/')

    else:  #Qui ci si entra in caso di prima di prima visualizzazione o richiesta GET
        form = formLogin()

    context = {'form' : form}
    return render(request,'login.html',context)


def addHotel (request):
    if request.method == 'POST':
        form = AddHotelForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            street = form.cleaned_data['street']
            houseNumber = form.cleaned_data['houseNumber']
            city = form.cleaned_data['city']
            zipCode = form.cleaned_data['zipCode']
            photoUrl = form.cleaned_data['photoUrl']

            adress = Address(street, houseNumber, city, zipCode)

            adress.save()

            hotel = Hotel(name, description, adress, photoUrl)

            hotel.save()

            return redirect('manageHotel')
    else:
        form = AddHotelForm()

    context = {'formAddHotel': form}
    return render(request, 'addHotel.html', context)


def addRoomToHotel(request):
    if request.method == 'POST':
        form = AddRoomForm(request.POST)
        if form.is_valid():
            form.save()

            roomNumber = form.cleaned_data['roomNumber']
            bedsNumber = form.cleaned_data['bedsNumber']

            hotel = Hotel.objects.all().filter(pk=request.getAttribute('hotelId'))

            services = [label for value, label in form.fields['services'].choices if value in form['services'].value()]

            price = form.cleaned_data['price']

            tmpRoom = Room(roomNumber, bedsNumber, price, hotel)
            tmpRoom.save()

            for s in services:
                temp = IncludedService(service=s,room=tmpRoom)
                temp.save()

            return redirect('addRoom')
    else:
        form = AddRoomForm()

    context = {'formAddRoom': form}
    return render(request, 'addRoom.html', context)



def notRegisteredHome(request):
    pass


def registerUser(request):
    pass

def registeredUserHome(request):
    pass

def searchResults(request):
    pass

def bookARoom(request):
    pass

def hotelKeeperHome(request):
    pass

def hotelsList(request):
    pass

def hotelDetail(request):
    pass