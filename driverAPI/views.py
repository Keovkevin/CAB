from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


import geopy.distance


from .models import  DriverLocation
from passengerAPI.models  import requestRide
from passengerAPI.serializers import PassengerInfoSerializer
from .serializers import  GetListOfAvailablePassengersSerializer
from .serializers import DriverLocationSerializer,acceptBookingSerializer

import logging

logger = logging.getLogger(__name__)


class GetDriverLocations(APIView):

    """
    This function gets the locations of all active drivers who are currently driving the cab

    """
    serializer_class = DriverLocationSerializer

    def get(self, request, format=None):
        driver_locations = DriverLocation.objects.all()
        serializer = DriverLocationSerializer(driver_locations, many=True)
        logger.info("getting latitude and longitude")
        return Response(serializer.data)

    def post(self, request, format=None):
        driver_id = request.session['driver_id']
        context = {"driver_id": driver_id}
        serializer = DriverLocationSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            logger.info("persisting data")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning("Invalid")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetListOfAvailablePassengers(APIView):

    """
    This function returns a list of available passengers, according the source address given by passenger
    Usage of library geopy for distance calculations b/n source and destinations

    """

    serializer_class = GetListOfAvailablePassengersSerializer


    def post(self, request, format=None):
        serializer = GetListOfAvailablePassengersSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):

            lat = request.data['Source_address']
            lon = request.data['Destination_address']

            passenger_locations = requestRide.objects.all()
            available_passenger_list = []
            distance_map = {}

            for location in passenger_locations:
                if location.booking_status == 0:

                    coords_1 = (lat, lon)
                    coords_2 = (location.latitude, location.longitude)
                    distance = geopy.distance.vincenty(coords_1, coords_2).km

                    distance_map[distance] = location

            for i in sorted(distance_map.keys()):
                logger.info("list iteration")
                available_passenger_list.append(distance_map[i])

            if available_passenger_list:
                serializer = PassengerInfoSerializer(available_passenger_list, many=True)
                return Response(serializer.data)
            else:
                data = {"Unavailable": "Sorry, no cabs are available at this time"}
                logger.warning("No Cabs")
                return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class acceptCab(APIView):

    """
    This function makes a request to accept cab by entering passenger_id,
    It also changes the booking status to 1
    And removes to available rides/cabs from the list
    """
    serializer_class = acceptBookingSerializer

    def post(self, request, format=None):
        passenger_id = request.data['passenger_id']
        all_rides = requestRide.objects.all()
        for ride in all_rides:
            if str(ride.passenger_id.passenger_id) == passenger_id:
                ride.booking_status = 1
                logger.warning("check data persists or not")
                ride.save()
                data = {
                    "Success": "Cab booked successfully"
                }
                return Response(data, status=status.HTTP_201_CREATED)
        errorMessage = {
            "Error": "Error"
        }
        return Response(errorMessage, status=status.HTTP_201_CREATED)

