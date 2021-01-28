from django.db import models

# Create your models here.

class MyClass(models.Model):
    name=models.CharField(max_length=12)