from django.shortcuts import render, redirect
from .forms import AddHotelForm
from .models import Hotel

# Create your views here.
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
