from django.contrib import admin
from .models import Record, Profile, IncidentType

# Register your models here.
admin.site.register(Record)
admin.site.register(Profile)
admin.site.register(IncidentType)