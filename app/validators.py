from rest_framework import serializers
from .models import Aircraft, Airport


def icao_validator(icao: str):
    airport = Airport.objects.filter(icao__iexact=icao)
    if not airport:
        raise serializers.ValidationError("Airport With ICAO does not exist.")


def aircraft_validator(ser_no: str):
    aircraft = Aircraft.objects.filter(serial_number__iexact=ser_no)
    if not aircraft:
        raise serializers.ValidationError("Aircraft with serial number does not exist.")
