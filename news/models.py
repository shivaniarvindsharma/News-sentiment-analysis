from django.db import models

class NewsArticle(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    sentiment = models.CharField(max_length=20, blank=True, null=True)          

    def __str__(self):
        return self.title

