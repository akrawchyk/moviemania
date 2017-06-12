# Movie Mania

## Initial Data

To load initial data you have 2 options. First is an example for how I
initially loaded the data into Django in order to generate fixtures:

```
python manage.py loaddata_movies_genres
```

or a more typical Django initial data loading (run in this order):

```
python manage.py loaddata genres.json
python manage.py loaddata movies.json
```

## Endpoints

```
/api/movies/
/api/movies/<pk>/

/api/genres/
/api/genres/<pk>/

/api/topGenreByYear/?year=<year>
```

## Description

Attached is a text file mapping movie information to it's genre
information. Using Django and Django REST Framework, we would like you
to do the following:

1. Load the `movies_genres.tsv` into the Django using a SQLite database.
2. Create a JSON REST API following the criteria below.


Core JSON REST API functionality:

1. A web api client should be able to create, retrieve, list, update,
and delete movies and genres
2. A web api client should be able to filter movies by genre
3. A web api client should be able to retrieve and list counts of
movies by genre


Additional insightful REST API functionality:

1. A web api client should be able to retrieve or list which genre had
the most movies per year.  The returned data should include the year,
genre name, and count.
2. A web api client should be able to retrieve or list movies that
include a "number of sequels" field based on whether this movie name
is a prefix of other movies.  For example, "The Godfather" is a prefix
of "The Godfather Part II" and "The Godfather Part III", so the REST
endpoint for "The Godfather" should show a sequel count of 2.  Note,
you can add this to the existing "movies" REST API from the core API
you wrote above.
