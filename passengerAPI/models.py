from lib2to3.pgen2.driver import Driver

from django.db import models


# Create your models here.
from django.db.models import DecimalField


class Passenger(models.Model):
    """
    Stores passenger info
    """
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    number = models.IntegerField(unique=True)

class setLocation(models.Model):
    """
    Storing Passengers Locations that are coming to server
    when driver is logged in into the application

    """
    passenger_id = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    latitude = DecimalField(max_digits=9, decimal_places=6)
    longitude = DecimalField(max_digits=9, decimal_places=6)

class requestRide(models.Model):
    passenger_id = models.IntegerField()
    driver_id = models.IntegerField()
    source_address = models.TextField()
    destination_address = models.TextField()
    booking_status = models.IntegerField()

# class isRideAccepted(models.Model):
#     isRideAccepted = models.IntegerField()