from django.contrib import admin
from django.utils.html import format_html
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminBase
from .models import Location, LocationImage
from tinymce.widgets import TinyMCE
from django import forms


class LocationAdminForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'
        widgets = {
            'description_long': TinyMCE(attrs={'cols': 80, 'rows': 30}),
        }


class LocationImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = LocationImage
    extra = 1
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 200px;"/>', obj.image.url)
        return 'Нет изображения'

    image_preview.short_description = 'Превью'


@admin.register(Location)
class LocationAdmin(SortableAdminBase, admin.ModelAdmin):
    form = LocationAdminForm
    list_display = ['title']
    inlines = [LocationImageInline]

@admin.register(LocationImage)
class LocationImageAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'location', 'order']
    list_filter = ['location']
    search_fields = ['location__title']
    readonly_fields = ('image_preview',)
    raw_id_fields = ('location',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image.url)
        return 'Нет изображения'

    image_preview.short_description = 'Превью'
