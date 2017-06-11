# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Count
from rest_framework import viewsets
from django_filters import rest_framework as filters

from movies.models import Movie, Genre
from movies.serializers import MovieSerializer, GenreSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all().order_by('-release_date')
    serializer_class = MovieSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('genres',)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.annotate(movie_count=Count('movie'))
    serializer_class = GenreSerializer
