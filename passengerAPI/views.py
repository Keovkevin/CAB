from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions

from functools import partial

from .models import Passenger, setLocation, requestRide
from .serializers import PassengerRegistrationSerializer, setLocationSerializer
from .serializers import PassengerLoginSerializer
from .serializers import requestRideSerializer



class CustomPermissionsForPassenger(permissions.BasePermission):

    def __init__(self, allowed_methods):
        self.allowed_methods = allowed_methods

    def has_permission(self, request, view):
        if 'passenger_id' in request.session.keys():
            return request.method in self.allowed_methods


class PassengerRegistration(APIView):
    """
    Register a Passenger

    """
    serializer_class = PassengerRegistrationSerializer

    def get(self, request, format=None):
        customers = Passenger.objects.all()
        serializer = PassengerRegistrationSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PassengerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PassengerLogin(APIView):

    serializer_class = PassengerLoginSerializer

    def post(self, request, format=None):
        serializer = PassengerLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            request.session['passenger_id'] = serializer.validated_data["passenger_id"]
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class  setLocation(APIView):

    """
    This function gets the locations of all active drivers who are currently driving the cab

    """
    serializer_class = setLocationSerializer
    permission_classes = (partial(CustomPermissionsForPassenger, ['GET', 'HEAD', 'POST']),)

    def get(self, request, format=None):
        driver_locations = setLocation.objects.all()
        serializer = setLocationSerializer(driver_locations, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        passenger_id = request.session['passenger_id']
        context = {"passenger_id": passenger_id}
        serializer = setLocationSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RequestRide(APIView):

    """
    This function makes a request to book cab by entering car_no,
    (selecting an available cab from map i.e tapping on it
    in real scenario) and arrange a ride.

    """
    serializer_class = requestRideSerializer
    permission_classes = (partial(CustomPermissionsForPassenger, ['GET', 'HEAD', 'POST']),)

    def post(self, request, format=None):
        context = {
            'passenger_id': request.session['passenger_id'],
            'source_address': request.session['source_address'],
            'destination_address': request.session['destination_address'],
            'booking_status': 0,
        }
        serializer = requestRideSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            data = {
                "Success": "Ride requested successfully"
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#
class isRideAccepted(APIView):
    def get(self, request, format=None):
        req = request.GET['passenger_id']
        ra = list(requestRide.objects.all())
        for e in ra:
           if e.passenger_id == req:
               return e.booking_status
        return -1


class Logout(APIView):

    def get(self, request, format=None):
        del request.session['passenger_id']
        data = {'Logout': 'logged out successfully'}
        return Response(data, status=status.HTTP_200_OK)

