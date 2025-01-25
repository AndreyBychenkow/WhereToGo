from django.contrib import admin
from .models import Location, LocationImage


class LocationImageInline(admin.TabularInline):
    model = LocationImage
    extra = 1
    fields = ('image', 'order')
    ordering = ('order',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('title', 'place_id', 'details_url')
    inlines = [LocationImageInline]


@admin.register(LocationImage)
class LocationImageAdmin(admin.ModelAdmin):
    list_display = ('location', 'image', 'order')
    list_editable = ('order',)
    ordering = ('order',)
