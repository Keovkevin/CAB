
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from .models import requestRide
from .serializers import setLocationSerializer
from .serializers import isRideAcceptedSerializer
from .serializers import PassengerInfoSerializer

import logging


logger = logging.getLogger(__name__)



class updateLocation(APIView):

    """
    This function sets the locations of all active passengers who are currently requesting the ride
    It accepts latitude and longitude as an input

    """
    serializer_class = setLocationSerializer

    def post(self, request, format=None):
        serializer = setLocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Data persists in the database")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestRide(APIView):

    """
    This function makes a request to ride  by entering passenger_id,latitude,longitude,driver_id

    """

    serializer_class = PassengerInfoSerializer

    def post(self, request, format=None):
        serializer = PassengerInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Data persists in the database")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#
class isRideAccepted(APIView):
    """
       This function makes a checks the booking_status  of ride is changed to 1 or still o by entering passenger_id
       And logging the info and warnings

    """

    serializer_class = isRideAcceptedSerializer

    def post(self, request, format=None):
        ride_id = request.data['passenger_id']

        all_rides = requestRide.objects.all()

        for ride in all_rides:
            if str(ride.passenger_id.passenger_id) == ride_id:
                data = {
                    "Status": ride.booking_status
                }
                logger.info("Status output")
                return Response(data, status=status.HTTP_201_CREATED)

        error = {
            "Error": "errorMessage"
        }
        logger.warning("Error")
        return Response(error, status=status.HTTP_400_BAD_REQUEST)


