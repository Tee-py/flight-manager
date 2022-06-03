from .views import AirCraftView
from django.urls import path

urlpatterns = [
    path('aircraft/', AirCraftView.as_view(), name="aircraft"),
]