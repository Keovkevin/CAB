from rest_framework import serializers
from rest_framework.exceptions import ValidationError


from .models import Passenger, setLocation, requestRide


class PassengerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = '__all__'


class PassengerLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if not email and password:
            raise ValidationError("Username and Password is required")
        try:
            passenger = Passenger.objects.get(email=email)
        except Passenger.DoesNotExist:
            raise ValidationError("This email address does not exist")
        if passenger.password == password:
            data["passenger_id"] = passenger.id
            return data
        else:
            raise ValidationError("Invalid credentials")

# class isRideAcceptedSerializer(serializers.Serializer):
#     class Meta:
#         model = isRideAccepted
#         fields = '__all__'


class setLocationSerializer(serializers.Serializer):
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        model = setLocation
        fields = '__all__'

    def create(self, validated_data):
       # passenger_id = self.context.get("passenger_id")
        passenger = Passenger.objects.get(pk=passenger_id)
        lat = validated_data.pop('latitude')
        lon = validated_data.pop('longitude')
        obj = setLocation()
        obj.passenger_id = passenger.id
        obj.latitude = lat
        obj.longitude = lon
        obj.save()
        return obj


class requestRideSerializer(serializers.Serializer):
    car_no = serializers.CharField()

    def validate(self, data):
        car_no = data.get("car_no")

        if not car_no:
            raise ValidationError("Car Number is required")
        try:
            driver = Passenger.objects.get(car_no=car_no)
        except Passenger.DoesNotExist:
            raise ValidationError("Car with this number does not exist")

        return data

    def create(self, validated_data):
        passenger_id = self.context.get("passenger_id")
        driver_id = None
        source = self.context.get("source_address")
        destination = self.context.get("destination_address")
        booking_status = self.context.get("booking_status")
        obj1 = requestRide()
        obj1.passenger_id = passenger_id
        obj1.driver_id = driver_id
        obj1.source = source
        obj1.destination = destination
        obj1.booking_status = booking_status
        obj1.save()
        return obj1