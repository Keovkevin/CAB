from django.urls import path
from . import views

app_name = 'passengerAPI'

urlpatterns = [

    path('register/', views.PassengerRegistration.as_view(), name='passenger-registration'),
    path('login/', views.PassengerLogin.as_view(), name='passenger-login'),
    path('logout/', views.Logout.as_view(), name='passenger-logout'),
    path('requestRide/', views.requestRide.as_view(), name='ridecab'),
    path('isRideAccepted/', views.isRideAccepted.as_view(), name='isRideAccepted'),




]