from django.contrib import admin
from .models import Location, LocationImage
from django.utils.safestring import mark_safe

class LocationImageInline(admin.TabularInline):
    model = LocationImage
    extra = 1

    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 200px;"/>')
        return "Нет изображения"

    image_preview.short_description = 'Превью'


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('title', 'place_id', 'details_url')
    inlines = [LocationImageInline]
