from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.exceptions import ValidationError
from django.db.models import Q
import datetime
from .serializers import (
    AirCraftSerializer,
    AirportSerializer,
    DepartureFlightSerializer,
    FlightListSerializer,
    CreateFlightSerializer,
    DepartureSearchSerializer,
)
from .permissions import IsUser, IsAdmin
from .models import Aircraft, Airport, Flight
from .utils import format_datetime_str


class AirCraftView(generics.ListCreateAPIView):

    """
    API FOR AIRCRAFT CRUD
    """

    serializer_class = AirCraftSerializer

    def get_permissions(self):
        method = self.request.method
        if method == "GET":
            perms = [IsUser | IsAdmin]
        else:
            perms = [IsAdmin]
        return [permission() for permission in perms]

    def get(self, request, uid: str = None):
        try:
            if uid:
                obj = Aircraft.objects.get(uid=uid)
                ser = AirCraftSerializer(obj)
            else:
                queryset = Aircraft.objects.all()
                ser = AirCraftSerializer(queryset, many=True)
        except (Aircraft.DoesNotExist, ValidationError):
            return Response(
                {"status": False, "message": "Aircraft Not Found."},
                status.HTTP_404_NOT_FOUND,
            )
        return Response({"status": True, "data": ser.data})

    def put(self, request, uid: str):
        try:
            obj = Aircraft.objects.get(uid=uid)
        except (Aircraft.DoesNotExist, ValidationError):
            return Response(
                {"status": False, "message": "Not Found"}, status.HTTP_404_NOT_FOUND
            )
        ser = AirCraftSerializer(
            data=request.data, instance=obj, partial=True, context={"request": request}
        )
        if not ser.is_valid():
            return Response(
                {"status": False, "message": "serializer error", "data": ser.errors},
                status.HTTP_400_BAD_REQUEST,
            )
        ser.save()
        return Response({"status": True, "message": "updated"})

    def delete(self, request, uid: str):
        try:
            Aircraft.objects.filter(uid=uid).delete()
        except ValidationError:
            return Response(
                {"status": False, "message": "Invalid UUID"},
                status.HTTP_400_BAD_REQUEST,
            )
        return Response({"status": True, "message": "Deleted"})


class AirPortView(generics.ListCreateAPIView):

    """API FOR AIRPORT CRUD"""

    serializer_class = AirportSerializer

    def get_permissions(self):
        method = self.request.method
        if method == "GET":
            perms = [IsUser | IsAdmin]
        else:
            perms = [IsAdmin]
        return [permission() for permission in perms]

    def get(self, request, uid: str = None):
        try:
            if uid:
                obj = Airport.objects.get(uid=uid)
                ser = AirportSerializer(obj)
            else:
                queryset = Airport.objects.all()
                ser = AirportSerializer(queryset, many=True)
        except (Airport.DoesNotExist, ValidationError):
            return Response(
                {"status": False, "message": "Aircraft Not Found."},
                status.HTTP_404_NOT_FOUND,
            )
        return Response({"status": True, "data": ser.data})

    def put(self, request, uid: str):
        try:
            obj = Airport.objects.get(uid=uid)
        except (Airport.DoesNotExist, ValidationError):
            return Response(
                {"status": False, "message": "Not Found"}, status.HTTP_404_NOT_FOUND
            )
        ser = AirportSerializer(
            data=request.data, instance=obj, partial=True, context={"request": request}
        )
        if not ser.is_valid():
            return Response(
                {"status": False, "message": "serializer error", "data": ser.errors},
                status.HTTP_400_BAD_REQUEST,
            )
        ser.save()
        return Response({"status": True, "message": "updated"})

    def delete(self, request, uid: str):
        try:
            Airport.objects.filter(uid=uid).delete()
        except ValidationError:
            return Response(
                {"status": False, "message": "Invalid UUID"},
                status.HTTP_400_BAD_REQUEST,
            )
        return Response({"status": True, "message": "Deleted"})


class FlightView(generics.ListCreateAPIView):

    """API FOR FLIGHT CRUD"""

    serializer_class = CreateFlightSerializer

    def get_permissions(self):
        method = self.request.method
        if method == "GET":
            perms = [IsUser | IsAdmin]
        else:
            perms = [IsAdmin]
        return [permission() for permission in perms]

    def get(self, request, uid: str = None):
        try:
            if uid:
                obj = Flight.objects.get(uid=uid)
                ser = FlightListSerializer(obj)
            else:
                queryset = Flight.objects.all()
                ser = FlightListSerializer(queryset, many=True)
        except (Flight.DoesNotExist, ValidationError):
            return Response(
                {"status": False, "message": "Aircraft Not Found."},
                status.HTTP_404_NOT_FOUND,
            )
        return Response({"status": True, "data": ser.data})

    def put(self, request, uid: str):
        try:
            obj = Flight.objects.get(uid=uid)
        except (Flight.DoesNotExist, ValidationError):
            return Response(
                {"status": False, "message": "Not Found"}, status.HTTP_404_NOT_FOUND
            )
        ser = CreateFlightSerializer(
            data=request.data, instance=obj, partial=True, context={"request": request}
        )
        if not ser.is_valid():
            return Response(
                {"status": False, "message": "serializer error", "data": ser.errors},
                status.HTTP_400_BAD_REQUEST,
            )
        ser.save()
        return Response({"status": True, "message": "updated"})

    def delete(self, request, uid: str):
        try:
            Flight.objects.filter(uid=uid).delete()
        except ValidationError:
            return Response(
                {"status": False, "message": "Invalid UUID"},
                status.HTTP_400_BAD_REQUEST,
            )
        return Response({"status": True, "message": "Deleted"})


@api_view(["GET"])
def flight_search(request):
    dept = request.GET.get("dept")  # search by departure icao
    arr = request.GET.get("arr")  # search by arrival icao
    dept_rng = request.GET.get("dept_rng")  # search by depature datetime range
    flights = None
    try:
        if dept:
            flights = Flight.objects.filter(departure__icao__iexact=dept)
        elif arr:
            flights = Flight.objects.filter(arrival__icao__iexact=arr)
        elif dept_rng:
            times = dept_rng.split(";")
            start = times[0]
            end = times[1]
            start_time = datetime.time(
                int(start.split(":")[0]), int(start.split(":")[1])
            )
            end_time = datetime.time(int(end.split(":")[0]), int(end.split(":")[1]))
            flights = Flight.objects.filter(
                departure_dt__time__gte=start_time, departure_dt__time__lte=end_time
            )
        else:
            return Response(
                {"status": False, "message": "No seach Parameters Entered"},
                status.HTTP_400_BAD_REQUEST,
            )
    except (TypeError, IndexError):
        return Response(
            {"status": False, "message": "Invalid time range"},
            status.HTTP_400_BAD_REQUEST,
        )
    ser = FlightListSerializer(flights, many=True)
    return Response({"status": True, "data": ser.data})


@api_view(["GET"])
def departure_search(request):
    try:
        interval = request.GET.get("interval").split(";")
        dept_str = interval[0]
        arr_str = interval[1]
        dept_dt = format_datetime_str(dept_str)
        arr_dt = format_datetime_str(arr_str)
    except (ValueError, IndexError, AttributeError):
        return Response(
            {"status": False, "message": "Invalid interval"},
            status.HTTP_400_BAD_REQUEST,
        )
    query = Q(departure_dt__gte=dept_dt) & Q(arrival_dt__lte=arr_dt)
    departures = (
        Flight.objects.select_related("departure").filter(query).distinct("departure")
    )
    ser = DepartureSearchSerializer(departures, many=True)
    return Response({"status": True, "data": ser.data})


@api_view(["GET"])
def departure_flights(request, uid: str):
    try:
        interval = request.GET.get("interval").split(";")
        dept_str = interval[0]
        arr_str = interval[1]
        dept_dt = format_datetime_str(dept_str)
        arr_dt = format_datetime_str(arr_str)
    except (ValueError, IndexError, AttributeError):
        return Response(
            {"status": False, "message": "Invalid interval"},
            status.HTTP_400_BAD_REQUEST,
        )
    query = (
        Q(departure_dt__gte=dept_dt) & Q(arrival_dt__lte=arr_dt) & Q(departure__uid=uid)
    )
    flights = Flight.objects.select_related("aircraft").filter(query)
    ser = DepartureFlightSerializer(flights, many=True)
    return Response({"status": True, "data": ser.data})
