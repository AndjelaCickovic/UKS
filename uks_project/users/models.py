from django.db import models
from django.contrib.auth.models import User
from projects_app.models import Project 

# Create your models here.
   
class AppUser(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    projects = models.ManyToManyField(Project)

    