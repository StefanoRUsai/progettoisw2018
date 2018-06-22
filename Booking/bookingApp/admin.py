from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(RegisteredUser)
admin.site.register(HotelKeeper)
admin.site.register(CreditCard)
admin.site.register(Address)
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Hotel)
admin.site.register(IncludedService)
