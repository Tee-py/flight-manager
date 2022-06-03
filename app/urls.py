from .views import AirCraftView
from django.urls import path
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh_token/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('aircraft/', AirCraftView.as_view(), name="aircraft"),
]