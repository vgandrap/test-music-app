from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Genre(models.Model):
	genre_id = models.IntegerField(default=0, db_index=True, unique=True)
	genre_type = models.CharField(max_length=200)

	def __str__(self):
		return self.genre_type

@python_2_unicode_compatible
class Track(models.Model):
	title_id = models.IntegerField(default=0, db_index=True, unique=True)
	title = models.CharField(max_length=200)
	rating = models.FloatField()
	# rating = models.DecimalField(max_digits=1, decimal_places=1)
	genre = models.ManyToManyField(Genre)

	def __str__(self):
		return self.title