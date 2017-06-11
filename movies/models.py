# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.functional import cached_property


class Movie(models.Model):
    title = models.CharField(max_length=255)
    release_date = models.DateField('date released')
    genres = models.ManyToManyField('Genre')

    def __str__(self):
        return '{} ({})'.format(self.title, self.release_date.strftime('%Y'))

    class Meta:
        ordering = ('release_date',)

    @cached_property
    def sequels_count(self):
        return Movie.objects.filter(title__startswith=self.title).count()-1


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
