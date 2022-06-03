from django.utils import timezone
from rest_framework import serializers
from .models import Aircraft, Airport, Flight, Location

class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        exclude = ("uid",)

class AirCraftSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        attrs['serial_number'] = attrs['serial_number'].upper()
        return super().validate(attrs)

    class Meta:
        model = Aircraft
        fields = "__all__"

class AirportSerializer(serializers.ModelSerializer):

    location = LocationSerializer()

    def validate(self, attrs):
        attrs['icao'] = attrs['icao'].upper() # convert icao to upper case
        return super().validate(attrs)

    def create(self, data):
        loc = Location.objects.create(**self.validated_data['location'])
        # save all icao in uppercase
        del data['location']
        return Airport.objects.create(**data, location=loc)

    class Meta:
        model = Airport
        fields = "__all__"

class FlightSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if data['arrival_dt'] < data['departure_dt'] or data['departure_dt'] < timezone.now():
            raise serializers.ValidationError(detail="Invalid arrival and depature datetimes")
        # A Flight Can Only Be Created If the Aircraft is not attatched to a pending or departed flight within the range of the arrival and departure date
        return data

    

    class Meta:
        model = Flight
        fields = "__all__"
