from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from functools import partial

from .models import Driver, DriverLocation
from .serializers import DriverRegistrationSerializer
from .serializers import DriverLoginSerializer
from .serializers import DriverLocationSerializer


class CustomPermissions(permissions.BasePermission):

    def __init__(self, allowed_methods):
        self.allowed_methods = allowed_methods

    def has_permission(self, request, view):
        if 'driver_id' in request.session.keys():
            return request.method in self.allowed_methods


class DriverRegistration(APIView):
    """
    Registering a Driver

    """
    serializer_class = DriverRegistrationSerializer

    def get(self, request, format=None):

        drivers = Driver.objects.all()
        serializer = DriverRegistrationSerializer(drivers, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DriverRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DriverLogin(APIView):

    """
    Log in a driver

    """
    serializer_class = DriverLoginSerializer

    def post(self, request, format=None):
        serializer = DriverLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            request.session['driver_id'] = serializer.validated_data["driver_id"]
            return Response(new_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetDriverLocations(APIView):

    """
    This function gets the locations of all active drivers who are currently driving the cab

    """
    serializer_class = DriverLocationSerializer
    permission_classes = (partial(CustomPermissions, ['GET', 'HEAD', 'POST']),)

    def get(self, request, format=None):
        driver_locations = DriverLocation.objects.all()
        serializer = DriverLocationSerializer(driver_locations, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        driver_id = request.session['driver_id']
        context = {"driver_id": driver_id}
        serializer = DriverLocationSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class GetListOfAvailableCab(APIView):
#
#     """
#     This function returns a list of available drivers, according the source address given by passenger
#     It uses geoencoding api of google maps to convert latitude, longitude to address and vice versa.
#     Calculating available cabs is done by calculating distance between source address and available cabs location.
#     If this distance is < 4 kms,  then these cabs are shown as available.
#
#     """
#
#     serializer_class = GetAvailableCabSerializer
#     permission_classes = (partial(CustomPermissionsForPassenger, ['GET', 'HEAD', 'POST']),)
#
#     def post(self, request, format=None):
#         serializer = GetAvailableRidesSerializer(data=request.data)
#
#         if serializer.is_valid(raise_exception=True):
#             gmaps = googlemaps.Client(key='AIzaSyALWKpmu1YBGDTS7waWGFdokZgYWYJIQtE')
#             request.session['source_address'] = request.data['Source_address']
#             request.session['destination_address'] = request.data['Destination_address']
#             geocode_result = gmaps.geocode(request.data['Source_address'])
#             lat = geocode_result[0]["geometry"]["location"]["lat"]
#             lon = geocode_result[0]["geometry"]["location"]["lng"]
#
#             driver_locations = DriverLocation.objects.all()
#             available_drivers_list = []
#             for location in driver_locations:
#                 coords_1 = (lat, lon)
#                 coords_2 = (location.latitude, location.longitude)
#                 distance = geopy.distance.vincenty(coords_1, coords_2).km
#                 if distance < 4:
#                     driver = location.driver_id
#                     available_drivers_list.append(driver)
#             if available_drivers_list:
#                 serializer = DriverInfoSerializer(available_drivers_list, many=True)
#                 return Response(serializer.data)
#             else:
#                 data = {"Unavailable": "Sorry, no cabs are available at this time"}
#                 return Response(data)
#             # return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class Logout(APIView):

    def get(self, request, format=None):
        del request.session['driver_id']
        data = {"logout": "logged out successfully"}
        return Response(data, status=status.HTTP_200_OK)
