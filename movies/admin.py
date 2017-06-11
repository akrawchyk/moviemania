# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from movies.models import Movie, Genre


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    date_hierarchy = 'release_date'
    filter_horizontal = ('genres',)
    list_display = ('title', 'year_released',)
    list_filter = ('genres',)

    def year_released(self, obj):
        return obj.release_date.strftime('%Y')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass
