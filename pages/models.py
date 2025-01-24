from django.db import models


class Location(models.Model):
	title = models.CharField(max_length=255)
	place_id = models.CharField(max_length=100, unique=True)
	details_url = models.URLField()

	def __str__(self):
		return self.title
