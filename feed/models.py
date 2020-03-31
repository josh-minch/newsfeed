from django.db import models

class Article(models.Model):
    category = models.CharField(max_length=100)
    title = models.TextField()
    source = models.TextField()
    description = models.TextField(null=True)
    url = models.URLField(null=True, max_length=1000)
    url_to_image = models.URLField(null=True, max_length=1000)
    pub_date = models.DateTimeField('date published', null=True)

    def __str__(self):
        return self.title
