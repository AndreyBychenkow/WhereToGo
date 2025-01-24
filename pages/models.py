from django.db import models


class Location(models.Model):
	title = models.CharField(max_length=255, verbose_name="Название")
	place_id = models.CharField(max_length=100, unique=True, verbose_name="Идентификатор места")
	details_url = models.URLField(verbose_name="URL для деталей")
	latitude = models.FloatField(blank=True, null=True, verbose_name="Широта")
	longitude = models.FloatField(blank=True, null=True, verbose_name="Долгота")

	class Meta:
		verbose_name = "Локация"
		verbose_name_plural = "Локации"

	def __str__(self):
		return self.title


class LocationImage(models.Model):
	location = models.ForeignKey(Location, related_name='images', on_delete=models.CASCADE, verbose_name="Локация")
	image = models.ImageField(upload_to='', verbose_name="Изображение")
	order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

	class Meta:
		ordering = ['order']
		verbose_name = "Изображение локации"
		verbose_name_plural = "Изображения локаций"

	def __str__(self):
		return f"Изображение для {self.location.title} ({self.order})"
