# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets

from movies.models import Movie, Genre
from movies.serializers import MovieSerializer, GenreSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all().order_by('-release_date')
    serializer_class = MovieSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
