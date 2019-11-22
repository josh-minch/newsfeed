from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField()
    url_to_image = models.URLField()
    pub_date = models.DateTimeField('date published')
