from django.db import models
from django.contrib.auth.models import AbstractUser

from feed.models import Article

class User(AbstractUser):
    favorites = models.ManyToManyField(Article, default=None, blank=True)
