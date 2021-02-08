from django.db import models

from users.models import AppUser
from django.utils.translation import gettext_lazy as _
# Create your models here.

class Role(models.TextChoices):
    OWNER = 'Owner', _('Owner')
    COOWNER = 'Coowner', _('Coowner')
    COLABORATOR = 'Colaborator', _('Colaborator')

class Repository(models.Model):
    name = models.CharField(max_length = 264)
    description = models.CharField(max_length = 264, blank = True)
    is_public = models.BooleanField()
    members = models.ManyToManyField(AppUser, through = 'RepositoryUser')

class RepositoryUser(models.Model):
    user = models.ForeignKey(AppUser, on_delete = models.CASCADE)
    repository = models.ForeignKey(Repository, related_name = 'users', on_delete = models.CASCADE)
    role = models.CharField(max_length=11, choices=Role.choices)
