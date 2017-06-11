from rest_framework import serializers

from movies.models import Movie, Genre


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Movie
        fields = ('title', 'release_date', 'genres', 'sequels_count')


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    movie_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Genre
        fields = ('name', 'movie_count')
