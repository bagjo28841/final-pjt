from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class ProReview(models.Model):
    title = models.CharField(max_length=100)
    movie_title = models.CharField(max_length=50)
    movie_id = models.IntegerField()
    rank = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_proreviews')