# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Movie(models.Model):
    objects = None
    title = models.CharField(max_length=128)
    genre = models.ForeignKey(Genre, on_delete=models.DO_NOTHING)
    rating = models.FloatField()
    duration = models.DurationField(null=False, auto_created=False, help_text="00:00:00")
    description = models.TextField()
    date = models.DateTimeField(help_text='Released date')
    image = models.FileField(upload_to="movie", default="default.png")

    def __str__(self):
        return self.title

    @property
    def sessions(self):
        return self.sessions_set.all()


class Seats(models.Model):
    objects = None
    seat_id = models.PositiveSmallIntegerField(blank=False, null=False, unique=False)
    row_id = models.PositiveSmallIntegerField(blank=False, null=False, unique=False)

    def __str__(self):
        return f"{self.row_id}-{self.seat_id}"


class Sessions(models.Model):
    objects = None
    date = models.DateTimeField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    adult = models.BooleanField()

    def __str__(self):
        return f"{self.date}"


class Tickets(models.Model):
    objects = None
    sold = models.BooleanField()
    seat = models.ForeignKey(Seats, on_delete=models.CASCADE)
    session = models.ForeignKey(Sessions, on_delete=models.CASCADE)
    price = models.FloatField()

def testcall():
    return 'test successfull'