from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import DEFAULT_DB_ALIAS, transaction
import pandas as pd

from movies.models import Movie, Genre


class Command(BaseCommand):
    help = 'Loads denormalized movies genres data into database'

    def handle(self, *args, **options):
        data_path = Path(__file__).parent.joinpath('movies_genres.tsv')

        # load tsv to pandas
        df = pd.read_csv(
            data_path,
            sep='\t',
            index_col=False,
            header=None,
            names=['title', 'release_date', 'genre'],
            parse_dates=['release_date'])

        # take all unique genres
        genres = pd.DataFrame(df.genre.unique(), columns=['name'])

        # normalize movies by unique (title, release_date), concatenate genres
        movies = df.groupby(
            ['title', 'release_date']).apply(
                lambda x: ','.join(x.genre)).reset_index()
        movies.columns = ['title', 'release_date', 'genres']

        with transaction.atomic(using=DEFAULT_DB_ALIAS):
            # need pk for genres first in order to save m2m fields on movies
            genre_objs = {}
            for genre in genres.itertuples():
                g, created = Genre.objects.get_or_create(name=genre.name)
                # cache genre objects to avoid lookups later
                genre_objs[genre.name] = g

            # create movies and associate with genres
            for movie in movies.itertuples():
                m, created = Movie.objects.get_or_create(
                    title=movie.title, release_date=movie.release_date)

                # link movies and genres
                movie_genres = movie.genres.split(',')
                for genre_name in movie_genres:
                    m.genres.add(genre_objs[genre_name])
                m.save()
