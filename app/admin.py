from django.contrib import admin
from .models import Aircraft, Airport, Location, Flight

admin.site.register(Aircraft)
admin.site.register(Airport)
admin.site.register(Location)
admin.site.register(Flight)
