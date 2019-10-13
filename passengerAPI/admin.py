from django.contrib import admin
from .models import Passenger, requestRide, setLocation

admin.site.register(Passenger)
admin.site.register(requestRide)
admin.site.register(setLocation)
