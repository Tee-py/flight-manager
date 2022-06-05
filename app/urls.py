from .views import (
    AirCraftView,
    AirPortView,
    FlightView,
    departure_flights,
    departure_search,
    flight_search,
)
from django.urls import path
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path("login/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh_token/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("aircraft/", AirCraftView.as_view(), name="aircraft"),
    path("aircraft/<str:uid>/", AirCraftView.as_view(), name="aircraft-dets"),
    path("airport/", AirPortView.as_view(), name="airport"),
    path("airport/<str:uid>/", AirPortView.as_view(), name="airport-dets"),
    path("flight/", FlightView.as_view(), name="flight"),
    path("flight/search/", flight_search, name="flight-search"),
    path("flight/<str:uid>/", FlightView.as_view(), name="flight-dets"),
    path("departures/search/", departure_search, name="departure-search"),
    path("departures/flights/<str:uid>/", departure_flights, name="departure-flights"),
]
