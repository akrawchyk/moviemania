# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date

from django.db.models import Count
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
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


@api_view(['GET'])
def topGenreByYearView(request):
    year = request.GET.get('year')

    if not year:
        return Response({'message': 'Required `year` query parameter'},
                        status=400)

    try:
        year = int(year)
    except:
        return Response({'message': 'Unexpected year, must be 4 digits'},
                        status=400)

    start = date(int(year)-1, 12, 31)
    end = date(int(year)+1, 1, 1)
    top_genre = Genre.objects.filter(
        movie__release_date__gt=start,
        movie__release_date__lt=end).annotate(
            c=Count('name')).order_by('-c').first()

    if top_genre:
        serializer = GenreSerializer(top_genre, context={'request': request})
        return Response(serializer.data)
    else:
        return Response({'message': 'No top genre found'}, status=404)
