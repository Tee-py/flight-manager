from django.utils import timezone
from django.db.models import Avg, F, fields
from rest_framework import serializers
from .models import Aircraft, Airport, Flight, Location
from .validators import aircraft_validator, icao_validator


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        exclude = ("uid",)


class AirCraftSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if "serial_number" in attrs:
            attrs["serial_number"] = attrs["serial_number"].upper()
        return super().validate(attrs)

    def update(self, instance, validated_data):
        validated_data["updated_at"] = timezone.now()
        return super().update(instance, validated_data)

    class Meta:
        model = Aircraft
        fields = "__all__"
        read_only_fields = (
            "uid",
            "created_at",
        )


class AirportSerializer(serializers.ModelSerializer):

    location = LocationSerializer()

    def validate(self, attrs):
        request = self.context["request"]
        if "icao" in attrs:
            attrs["icao"] = attrs["icao"].upper()
        return super().validate(attrs)

    def create(self, data):
        loc = Location.objects.create(**self.validated_data["location"])
        del data["location"]
        return Airport.objects.create(**data, location=loc)

    def update(self, instance, validated_data):
        validated_data["updated_at"] = timezone.now()
        return super().update(instance, validated_data)

    class Meta:
        model = Airport
        fields = "__all__"
        read_only_fields = ("uid", "created_at", "location")


class FlightListSerializer(serializers.ModelSerializer):
    aircraft = AirCraftSerializer()
    departure = AirportSerializer()
    arrival = AirportSerializer()

    class Meta:
        model = Flight
        fields = "__all__"


class CreateFlightSerializer(serializers.ModelSerializer):

    aircraft = serializers.CharField(validators=[aircraft_validator], required=False)
    departure = serializers.CharField(validators=[icao_validator])
    arrival = serializers.CharField(validators=[icao_validator])

    def validate(self, attrs):
        if "arrival_dt" in attrs and "departure_dt" in attrs:
            # Date Time Validations on Creation
            if (
                attrs["arrival_dt"] < attrs["departure_dt"]
                or attrs["departure_dt"] < timezone.now()
            ):
                raise serializers.ValidationError(
                    detail="Invalid arrival and depature datetimes"
                )
        return attrs

    def create(self, validated_data):
        # Get the arrival, departure and aircraft objects
        arr = Airport.objects.filter(icao__icontains=validated_data["arrival"]).first()
        dept = Airport.objects.filter(
            icao__icontains=validated_data["departure"]
        ).first()
        validated_data["arrival"] = arr
        validated_data["departure"] = dept
        if "aircraft" in validated_data:
            craft = Aircraft.objects.filter(
                serial_number__icontains=validated_data["aircraft"]
            ).first()
            validated_data["aircraft"] = craft

        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "arrival" in validated_data:
            arr = Airport.objects.filter(
                icao__icontains=validated_data["arrival"]
            ).first()
            validated_data["arrival"] = arr
        if "departure" in validated_data:
            dept = Airport.objects.filter(
                icao__icontains=validated_data["departure"]
            ).first()
            validated_data["departure"] = dept
        if "aircraft" in validated_data:
            craft = Aircraft.objects.filter(
                serial_number__icontains=validated_data["aircraft"]
            ).first()
            validated_data["aircraft"] = craft
        return super().update(instance, validated_data)

    class Meta:
        model = Flight
        fields = "__all__"


class DepartureSearchSerializer(serializers.Serializer):

    uid = serializers.SerializerMethodField()
    icao = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    flight_count = serializers.SerializerMethodField()
    inflight_avg = serializers.SerializerMethodField()

    def get_uid(self, obj):
        return obj.departure.uid

    def get_icao(self, obj):
        return obj.departure.icao

    def get_name(self, obj):
        return obj.departure.name

    def get_flight_count(self, obj):
        return obj.departure.flight_departures.count()

    def get_inflight_avg(self, obj):
        qs = obj.departure.flight_departures.aggregate(
            inflight_avg=Avg(
                F("arrival_dt") - F("departure_dt"), output_filed=fields.DurationField()
            )
        )
        return qs["inflight_avg"].total_seconds() / 60 if qs["inflight_avg"] else 0


class DepartureFlightSerializer(serializers.ModelSerializer):

    inflight_time = serializers.SerializerMethodField()
    aircraft = AirCraftSerializer()

    def get_inflight_time(self, obj):
        return obj.get_inflight_time()

    class Meta:
        model = Flight
        fields = ("uid", "aircraft", "inflight_time", "departure_dt", "arrival_dt")
