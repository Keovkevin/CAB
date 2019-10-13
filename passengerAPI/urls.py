from django.urls import path
from . import views

app_name = 'passengerAPI'

urlpatterns = [

    path('RequestRide/', views.RequestRide.as_view(), name='ridecab'),
    path('isRideAccepted/', views.isRideAccepted.as_view(), name='isRideAccepted'),
    path('setLocation/', views.updateLocation.as_view(), name='setLocation'),




]