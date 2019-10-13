from django.urls import path
from . import views

app_name = 'driverAPI'

urlpatterns = [

    path('send_location/', views.GetDriverLocations.as_view(), name='driver-location'),
    path('available_passengers/', views.GetListOfAvailablePassengers.as_view(), name='getlistofavailablecab'),
    path('accept_cab/', views.acceptCab.as_view(), name='accept-cab'),

]
