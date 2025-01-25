from django.contrib import admin
from .models import Location, LocationImage


class LocationImageInline(admin.TabularInline):
    model = LocationImage
    extra = 0


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('title', 'place_id', 'details_url')
    inlines = [LocationImageInline]
