from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=100)
    movie_id = models.IntegerField()
    release_date = models.DateField()
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    overview = models.TextField()
    poster_path = models.CharField(max_length=200)
    genres = models.TextField()
