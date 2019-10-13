
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/v1/passenger/', include('passengerAPI.urls')),
    path('api/v1/driver/', include('driverAPI.urls')),
    path('admin/', admin.site.urls),
]
