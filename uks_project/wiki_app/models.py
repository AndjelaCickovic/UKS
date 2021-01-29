from django.db import models

class Wiki(models.Model):
    title = models.CharField(max_length=264)

class Page(models.Model):
    title = models.CharField(max_length=264)
    content = models.TextField()
    message = models.CharField(max_length=264, blank=True)
    wiki = models.ForeignKey(Wiki, on_delete=models.CASCADE)

# Create your models here.