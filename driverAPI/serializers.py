from rest_framework import serializers
from .models import Driver, DriverLocation


class DriverLocationSerializer(serializers.Serializer):
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        model = DriverLocation
        fields = '__all__'

    def create(self, validated_data):
        driver_id = self.context.get("driver_id")
        driver = Driver.objects.get(pk=driver_id)
        lat = validated_data.pop('latitude')
        lon = validated_data.pop('longitude')
        obj = DriverLocation()
        obj.driver_id = driver
        obj.latitude = lat
        obj.longitude = lon
        obj.save()
        return obj


class GetListOfAvailablePassengersSerializer(serializers.Serializer):
    Source_address = serializers.CharField()
    Destination_address = serializers.CharField()

    def validate(self, data):
        return data

class acceptBookingSerializer(serializers.Serializer):
    passenger_id = serializers.IntegerField()

    def validate(self, data):
        return data



