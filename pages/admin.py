from django.contrib import admin
from .models import Location, LocationImage


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
	list_display = ('title', 'place_id', 'details_url')


@admin.register(LocationImage)
class LocationImageAdmin(admin.ModelAdmin):
	list_display = ('location', 'image', 'order')
	list_editable = ('order',)
