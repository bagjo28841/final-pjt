from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    followers = models.ManyToManyField('self', symmetrical=False, related_name='followings')
    user_rank = models.IntegerField(default=1)


class Stamp(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # 기본 1개
    bonus = models.BooleanField(default=False)
    # 장르 19개
    action = models.BooleanField(default=False)
    adventure = models.BooleanField(default=False)
    animation = models.BooleanField(default=False)
    comedy = models.BooleanField(default=False)
    crime = models.BooleanField(default=False)
    documentary = models.BooleanField(default=False)
    drama = models.BooleanField(default=False)
    family = models.BooleanField(default=False)
    fantasy = models.BooleanField(default=False)
    history = models.BooleanField(default=False)
    horror = models.BooleanField(default=False)
    music = models.BooleanField(default=False)
    mystery = models.BooleanField(default=False)
    romance = models.BooleanField(default=False)
    science_fiction = models.BooleanField(default=False)
    tv_movie = models.BooleanField(default=False)
    thriller = models.BooleanField(default=False)
    war = models.BooleanField(default=False)
    western = models.BooleanField(default=False)
    # 추가 5개
    review_stamp = models.BooleanField(default=False)
    comment_stamp = models.BooleanField(default=False)
    follower_stamp = models.BooleanField(default=False)
    joined_stamp = models.BooleanField(default=False)
    all_stamp = models.BooleanField(default=False)