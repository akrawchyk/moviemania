# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.test import TestCase
from rest_framework.test import APIClient, APITransactionTestCase

from django.contrib.auth.models import User
from movies.models import Movie, Genre


class MoviesAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='test', email='test@test.com', password='top_secret')
        self.expected_genre = Genre.objects.create(name='Test Movie Genre')
        self.test_movie_data = {
            'title': 'Hydrogen',
            'release_date': '2006-01-01',
            'genres': ['/api/genres/{}/'.format(self.expected_genre.id)]}

    # create
    def test_movie_logged_create(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/movies/',
                                    self.test_movie_data, format='json')
        self.client.force_authenticate(user=None)
        data = response.data
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data.get('title'), self.test_movie_data['title'])
        self.assertEqual(data.get('release_date'),
                         self.test_movie_data['release_date'])
        self.assertTrue('/genres/{}'.format(self.expected_genre.id) in
                        ','.join(data.get('genres')))

    def test_movie_anon_create(self):
        response = self.client.post('/api/movies/', self.test_movie_data,
                                    format='json')
        self.assertEqual(response.status_code, 403)

    # read
    def test_movie_logged_read(self):
        test_movie = Movie.objects.create(
            title=self.test_movie_data['title'],
            release_date=self.test_movie_data['release_date'])
        test_movie.genres.add(self.expected_genre.id)
        test_movie.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            '/api/movies/{}/'.format(test_movie.id), format='json')
        self.client.force_authenticate(user=None)
        data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get('title'), self.test_movie_data['title'])
        self.assertEqual(data.get('release_date'),
                         self.test_movie_data['release_date'])

    def test_movie_anon_read(self):
        test_movie = Movie.objects.create(
            title=self.test_movie_data['title'],
            release_date=self.test_movie_data['release_date'])
        test_movie.genres.add(self.expected_genre.id)
        test_movie.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            '/api/movies/{}/'.format(test_movie.id), format='json')
        data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get('title'), self.test_movie_data['title'])
        self.assertEqual(data.get('release_date'),
                         self.test_movie_data['release_date'])

    # update
    def test_movie_logged_update(self):
        test_movie = Movie.objects.create(
            title=self.test_movie_data['title'],
            release_date=self.test_movie_data['release_date'])
        test_movie.genres.add(self.expected_genre.id)
        test_movie.save()
        expected_movie_data = {
            'title': 'Updated Title',
            'release_date': '1970-01-01',
            'genres': ['/api/genres/{}/'.format(self.expected_genre.id)]
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(
            '/api/movies/{}/'.format(test_movie.id),
            expected_movie_data, format='json')
        self.client.force_authenticate(user=None)
        data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get('title'), expected_movie_data['title'])
        self.assertEqual(data.get('release_date'),
                         expected_movie_data['release_date'])

    def test_movie_anon_update(self):
        test_movie = Movie.objects.create(
            title=self.test_movie_data['title'],
            release_date=self.test_movie_data['release_date'])
        test_movie.genres.add(self.expected_genre.id)
        test_movie.save()
        expected_movie_data = {
            'title': 'Updated Title',
            'release_date': '1970-01-01',
            'genres': ['/api/genres/{}/'.format(self.expected_genre.id)]
        }
        response = self.client.put(
            '/api/movies/{}/'.format(test_movie.id),
            expected_movie_data, format='json')
        self.assertEqual(response.status_code, 403)

    # delete
    def test_movie_logged_delete(self):
        test_movie = Movie.objects.create(
            title=self.test_movie_data['title'],
            release_date=self.test_movie_data['release_date'])
        test_movie.genres.add(self.expected_genre.id)
        test_movie.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            '/api/movies/{}/'.format(test_movie.id), format='json')
        self.client.force_authenticate(user=None)
        self.assertEqual(response.status_code, 204)

    def test_movie_anon_delete(self):
        test_movie = Movie.objects.create(
            title=self.test_movie_data['title'],
            release_date=self.test_movie_data['release_date'])
        test_movie.genres.add(self.expected_genre.id)
        test_movie.save()
        response = self.client.delete(
            '/api/movies/{}/'.format(test_movie.id), format='json')
        self.assertEqual(response.status_code, 403)

    # list
    def test_movie_logged_list(self):
        test_movies = ['Helium', 'Neon', 'Argon', 'Krypton', 'Xenon', 'Radon']
        for movie in test_movies:
            m = Movie.objects.create(
                title=movie, release_date=self.test_movie_data['release_date'])
            m.genres.add(self.expected_genre)
            m.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/movies/', format='json')
        self.client.force_authenticate(user=None)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'), len(test_movies))

    def test_movie_anon_list(self):
        test_movies = ['Helium', 'Neon', 'Argon', 'Krypton', 'Xenon', 'Radon']
        for movie in test_movies:
            m = Movie.objects.create(
                title=movie, release_date=self.test_movie_data['release_date'])
            m.genres.add(self.expected_genre)
            m.save()
        response = self.client.get('/api/movies/', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'), len(test_movies))

    # filter by genre
    def test_movie_genre_filter(self):
        test_movies = ['Helium', 'Neon', 'Argon', 'Krypton', 'Xenon', 'Radon']
        another_genre = Genre.objects.create(name='Another Genre')
        for idx, movie in enumerate(test_movies):
            m = Movie.objects.create(
                title=movie, release_date=self.test_movie_data['release_date'])
            if idx % 2 > 0:
                m.genres.add(self.expected_genre)
            else:
                m.genres.add(another_genre)
            m.save()
        # single filter
        response = self.client.get(
            '/api/movies/?genres={}'.format(another_genre.id), format='json')
        data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get('count'), 3)
        # multiple filter
        response = self.client.get(
            '/api/movies/?genres={}&genres={}'.format(
                self.expected_genre.id, another_genre.id), format='json')
        data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get('count'), 6)

    # sequels count
    def test_movie_sequels_count(self):
        test_movies = ['The Godfather', 'The Godfather Part II',
                       'The Godfather Part III']
        movies = []
        for movie in test_movies:
            m = Movie.objects.create(
                title=movie, release_date=self.test_movie_data['release_date'])
            m.genres.add(self.expected_genre)
            m.save()
            movies.append(m)
        # sequels
        response = self.client.get('/api/movies/{}/'.format(movies[0].id),
                                   format='json')
        data = response.data
        self.assertEqual(data.get('sequels_count'), 2)
        response = self.client.get('/api/movies/{}/'.format(movies[1].id),
                                   format='json')
        data = response.data
        self.assertEqual(data.get('sequels_count'), 1)
        # no sequels
        response = self.client.get('/api/movies/{}/'.format(movies[2].id),
                                   format='json')
        data = response.data
        self.assertEqual(data.get('sequels_count'), 0)


class GenreAPITestCase(APITransactionTestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='test', email='test@test.com', password='top_secret')

    # create
    def test_genre_logged_create(self):
        expected_name = 'Test Genre'
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            '/api/genres/', {'name': expected_name}, format='json')
        self.client.force_authenticate(user=None)
        test_genre = Genre.objects.get(name=expected_name)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(test_genre.name, expected_name)

    def test_genre_anon_create(self):
        expected_name = 'Test Genre'
        response = self.client.post(
            '/api/genres/', {'name': expected_name}, format='json')
        self.assertEqual(response.status_code, 403)

    # read
    def test_genre_logged_read(self):
        expected_name = 'Test Genre'
        test_genre = Genre.objects.create(name=expected_name)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            '/api/genres/{}/'.format(test_genre.id), format='json')
        self.client.force_authenticate(user=None)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('name'), expected_name)

    def test_genre_anon_read(self):
        expected_name = 'Test Genre'
        test_genre = Genre.objects.create(name=expected_name)
        response = self.client.get(
            '/api/genres/{}/'.format(test_genre.id), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('name'), expected_name)

    # update
    def test_genre_logged_update(self):
        initial_name = 'Test Genre'
        expected_name = 'Updated Genre'
        test_genre = Genre.objects.create(name=initial_name)
        self.client.force_authenticate(user=self.user)
        response = self.client.put(
            '/api/genres/{}/'.format(test_genre.id), {'name': expected_name},
            format='json')
        self.client.force_authenticate(user=None)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('name'), expected_name)

    def test_genre_anon_update(self):
        initial_name = 'Test Genre'
        expected_name = 'Updated Genre'
        test_genre = Genre.objects.create(name=initial_name)
        response = self.client.put(
            '/api/genres/{}/'.format(test_genre.id), {'name': expected_name},
            format='json')
        self.assertEqual(response.status_code, 403)

    # delete
    def test_genre_logged_delete(self):
        test_genre = Genre.objects.create(name='Test Genre')
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            '/api/genres/{}/'.format(test_genre.id), format='json')
        self.client.force_authenticate(user=None)
        self.assertEqual(response.status_code, 204)

    def test_genre_anon_delete(self):
        test_genre = Genre.objects.create(name='Test Genre')
        response = self.client.delete(
            '/api/genres/{}/'.format(test_genre.id), format='json')
        self.assertEqual(response.status_code, 403)

    # list
    def test_genre_logged_list(self):
        test_genres = ['Helium', 'Neon', 'Argon', 'Krypton', 'Xenon', 'Radon']
        for genre_name in test_genres:
            Genre.objects.create(name=genre_name)
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/genres/', format='json')
        self.client.force_authenticate(user=None)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'), len(test_genres))

    def test_genre_anon_list(self):
        test_genres = ['Helium', 'Neon', 'Argon', 'Krypton', 'Xenon', 'Radon']
        for genre_name in test_genres:
            Genre.objects.create(name=genre_name)
        response = self.client.get('/api/genres/', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'), len(test_genres))

    # movie counts
    def test_genre_movie_count(self):
        test_genre = Genre.objects.create(name='Test Genre')
        another_genre = Genre.objects.create(name='Another Genre')
        test_movies = ['Helium', 'Neon', 'Argon', 'Krypton', 'Xenon', 'Radon']
        for idx, movie in enumerate(test_movies):
            test_movie_data = {
                'title': movie,
                'release_date': '2006-01-01'}
            m = Movie.objects.create(**test_movie_data)
            if idx % 2 > 0:
                m.genres.add(test_genre)
            else:
                m.genres.add(another_genre)
            m.save()

        response = self.client.get('/api/genres/{}/'.format(test_genre.id),
                                   format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('movie_count'), 3)


class TopGenreByYearTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        test_genres = ['Earth', 'Fire', 'Wind']
        test_movies = ['Helium', 'Neon', 'Argon', 'Krypton', 'Xenon', 'Radon']
        years = [2999, 3000, 3001]

        genres = []
        for genre in test_genres:
            g = Genre.objects.create(name=genre)
            genres.append(g)

        for y in years:
            for idx, movie in enumerate(test_movies):
                m = Movie.objects.create(title=movie,
                                         release_date='{}-01-01'.format(y))
                if y == 3001:
                    m.genres.add(genres[2])
                elif idx % 2 > 0:
                    m.genres.add(genres[0])
                else:
                    m.genres.add(genres[1])

    def test_top_genre_by_year(self):
        response = self.client.get('/api/topGenreByYear/?year=3001', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('name'), 'Wind')
        response = self.client.get('/api/topGenreByYear/?year=3000', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('name'), 'Earth')

    def test_top_genre_by_year_no_movies(self):
        response = self.client.get('/api/topGenreByYear/?year=1800', format='json')
        self.assertEqual(response.status_code, 404)

    def test_top_genre_by_year_no_year_input(self):
        response = self.client.get('/api/topGenreByYear/', format='json')
        self.assertEqual(response.status_code, 400)

    def test_top_genre_by_year_bad_year_input(self):
        response = self.client.get('/api/topGenreByYear/?year=asdf', format='json')
        self.assertEqual(response.status_code, 400)
