from django.db import models
from tinymce import models as tinymce_models


class Location(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    latitude = models.FloatField(default=0.0, verbose_name="Широта")
    longitude = models.FloatField(default=0.0,verbose_name="Долгота")
    short_description = models.TextField(verbose_name="Краткое описание", blank=True, null=True)
    long_description = tinymce_models.HTMLField(verbose_name="Полное описание", blank=True, null=True)

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"

    def __str__(self):
        return self.title


class LocationImage(models.Model):
    image = models.ImageField(verbose_name="Изображение")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    location = models.ForeignKey(
        Location,
        related_name='images',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Связанная локация"
    )

    class Meta:
        ordering = ['order']
        verbose_name = "Изображение локации"
        verbose_name_plural = "Изображения локаций"

    def __str__(self):
        location_info = f" для {self.location.title}" if self.location else " (независимое изображение)"
        return f"Изображение{location_info} ({self.order})"
