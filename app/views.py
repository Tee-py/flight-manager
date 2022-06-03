from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from .serializers import AirCraftSerializer
from .permissions import IsUser, IsAdmin
from .models import Aircraft, Airport, Flight


class AirCraftView(generics.ListCreateAPIView):

    """
    API FOR AIRCRAFT CRUD
    1. Fetch All Aircrafts
    2. Create Aircraft
    3. Retrieve Aircraft
    """

    queryset = Aircraft.objects.all()
    serializer_class = AirCraftSerializer
    permission_classes = [IsAdminUser]


class AirportView(generics.ListCreateAPIView):
    pass


