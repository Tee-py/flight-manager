from django.contrib import admin
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.urls import path, include


@api_view(["GET"])
@permission_classes([])
def root(request):
    return Response({"status": True, "message": "OK 👋"})


urlpatterns = [
    path("", root, name="root"),
    path("admin/", admin.site.urls),
    path("api/", include("app.urls")),
]
