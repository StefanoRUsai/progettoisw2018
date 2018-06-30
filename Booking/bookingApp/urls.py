from django.urls import path
from . import views as v

urlpatterns = [
    path('', v.notRegisteredHome),
    path('addRoom/', v.addRoomToHotel),
    path('login/', v.login),
    path('profile/', v.viewProfileClient),
    path('signUp/', v.registerClient),
    path('homeRegistered/', v.registeredClientHome),
    path('search/', v.searchResults),
    path('booking/', v.bookARoom),
    path('home/', v.hotelKeeperHome),  # ho lasciato home perchè dai disegni delle specifiche si vede così
    path('hotels/', v.hotelsList),  # ho lasciato hotels perchè dai disegni delle specifiche si vede così
    path('addHotel/', v.addHotel),
    path('hotel/', v.hotelDetail),
    path('searchbar/', v.searchBar),
    path('logout/', v.logoutView)
]
