from rest_framework import serializers
from .models import setLocation, requestRide


class isRideAcceptedSerializer(serializers.Serializer):
    passenger_id = serializers.IntegerField()


class setLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = setLocation
        fields = '__all__'

class requestRideSerializer(serializers.Serializer):
    class Meta:
        model = requestRide
        fields = '__all__'

class PassengerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = requestRide
        fields = '__all__'