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

    # create
    def test_movie_logged_create(self):
        expected_title = 'Hydrogen'
        expected_release_date = '2006-01-01'
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            '/api/movies/',
            {'title': expected_title,
             'release_date': expected_release_date,
             'genres': ['/api/genres/{}/'.format(self.expected_genre.id)]},
            format='json')
        self.client.force_authenticate(user=None)
        test_movie = Movie.objects.get(title=expected_title)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(test_movie.title, expected_title)
        self.assertEqual(test_movie.release_date, datetime.date(2006, 1, 1))
        self.assertEqual(test_movie.genres.first().id, self.expected_genre.id)

    def test_movie_anon_create(self):
        expected_title = 'Hydrogen'
        expected_release_date = '2006-01-01'
        response = self.client.post(
            '/api/movies/',
            {'title': expected_title,
             'release_date': expected_release_date,
             'genres': [self.expected_genre.id]}, format='json')
        self.assertEqual(response.status_code, 403)

    # read
    def test_movie_logged_read(self):
        pass

    def test_movie_anon_read(self):
        pass

    # update
    def test_movie_logged_update(self):
        pass

    def test_movie_anon_update(self):
        pass

    # dlete
    def test_movie_logged_delete(self):
        pass

    def test_movie_anon_delete(self):
        pass

    # list
    def test_movie_logged_list(self):
        pass

    def test_movie_anon_list(self):
        pass


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
        self.assertEqual(response.data.get('name'), expected_name)

    def test_genre_anon_read(self):
        expected_name = 'Test Genre'
        test_genre = Genre.objects.create(name=expected_name)
        response = self.client.get(
            '/api/genres/{}/'.format(test_genre.id), format='json')
        self.assertEqual(response.data.get('name'), expected_name)

    # update
    def test_genre_logged_read(self):
        initial_name = 'Test Genre'
        expected_name = 'Updated Genre'
        test_genre = Genre.objects.create(name=initial_name)
        self.client.force_authenticate(user=self.user)
        response = self.client.put(
            '/api/genres/{}/'.format(test_genre.id), {'name': expected_name},
            format='json')
        self.client.force_authenticate(user=None)
        self.assertEqual(response.data.get('name'), expected_name)

    def test_genre_anon_read(self):
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
        self.assertEqual(response.data.get('count'), len(test_genres))

    def test_genre_anon_list(self):
        test_genres = ['Helium', 'Neon', 'Argon', 'Krypton', 'Xenon', 'Radon']
        for genre_name in test_genres:
            Genre.objects.create(name=genre_name)
        response = self.client.get('/api/genres/', format='json')
        self.assertEqual(response.data.get('count'), len(test_genres))
