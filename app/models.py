from django.db import models
from django.utils import timezone
import uuid
from django.contrib.auth.models import AbstractUser
from .managers import UserManager


class BaseModel(models.Model):

    uid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True)

    class Meta:
        abstract = True


class User(BaseModel, AbstractUser):

    ROLE_CHOICES = (("user", "user"), ("admin", "admin"))

    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.get_full_name()


class Location(models.Model):

    uid = models.UUIDField(default=uuid.uuid4)
    area = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    lat = models.DecimalField(max_digits=12, decimal_places=4)
    lng = models.DecimalField(max_digits=12, decimal_places=4)


class Airport(BaseModel):

    name = models.CharField(max_length=100)
    icao = models.CharField(max_length=10, unique=True)
    location = models.OneToOneField(Location, on_delete=models.SET_NULL, null=True)


class Aircraft(BaseModel):

    serial_number = models.CharField(max_length=100, unique=True)
    manufacturer = models.TextField()


class Flight(BaseModel):

    STATUS_CHOICES = (
        ("scheduled", "scheduled"),
        ("departed", "departed"),
        ("arrived", "arrived"),
        ("cancelled", "cancelled"),
    )

    aircraft = models.ForeignKey(
        Aircraft, on_delete=models.SET_NULL, null=True, related_name="flights"
    )
    departure = models.ForeignKey(
        Airport, on_delete=models.DO_NOTHING, related_name="flight_departures"
    )
    arrival = models.ForeignKey(
        Airport, on_delete=models.DO_NOTHING, related_name="flight_arrivals"
    )
    departure_dt = models.DateTimeField()
    arrival_dt = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    def get_inflight_time(self):
        return (self.arrival_dt - self.departure_dt).total_seconds() / 60
