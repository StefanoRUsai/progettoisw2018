from django.contrib import admin
from django.urls import path
from . import views as v

urlpatterns = [
    path('', v.notRegisteredHome),
    path('login/', v.loginPage),
    path('signUp/', v.registerUser),
    path('homeRegistered/', v.registeredUserHome),
    path('search/', v.searchResults),
    path('booking/', v.bookARoom),
    path('home/', v.hotelKeeperHome), #ho lasciato home perchè dai disegni delle specifiche si vede così
    path('hotels/', v.hotelsList), #ho lasciato hotels perchè dai disegni delle specifiche si vede così
    path('addHotel', v.addHotel),
    path('hotel/', v.hotelDetail),
    path('addRoom/', v.addRoomToHotel),

]
