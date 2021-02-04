from django.db import models
from projects_app.models import Project
from branches_app.models import Branch 
from users.models import User
from django.utils.translation import gettext_lazy as _
# Create your models here.

class Role(models.TextChoices):
    OWNER = 'Owner', _('Owner')
    COLABORATOR = 'Colaborator', _('Colaborator')


class RepositoryUser(models.Model):
    user = models.ForeignKey(User, related_name = 'app_user', on_delete = models.DO_NOTHING)
    role = models.CharField(max_length=11, choices=Role.choices)


class Repository(models.Model):
    name = models.CharField(max_length = 264)
    description = models.CharField(max_length = 264, blank = True)
    is_public = models.BooleanField()