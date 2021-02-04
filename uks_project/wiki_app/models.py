from django.db import models
from repositories.models import Repository

class Wiki(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)

class Page(models.Model):
    title = models.CharField(max_length=264)
    content = models.TextField()
    message = models.CharField(max_length=264, blank=True)
    wiki = models.ForeignKey(Wiki, on_delete=models.CASCADE)