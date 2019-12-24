from django.db import models

class Article(models.Model):
    category = models.CharField(max_length=200)
    title = models.CharField(max_length=200, null=True)
    source = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    url = models.URLField(null=True)
    url_to_image = models.URLField(null=True)
    pub_date = models.DateTimeField('date published', null=True)

    def __str__(self):
        return self.title
