from django.db import models

# Create your models here.

class Repository(models.Model):
    name = models.CharField(max_length = 264)
    description = models.CharField(max_length = 264, blank = True)
    is_public = models.BooleanField()