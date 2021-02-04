from django.db import models
from wiki_app.models import Wiki 
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
    #repository = models.ForeignKey(Repository, related_name = 'repository', on_delete = models.DO_NOTHING)
    # user treba prosiriti sa repositories 
    role = models.CharField(max_length=11, choices=Role.choices)


class Repository(models.Model):
    name = models.CharField(max_length = 264)
    description = models.CharField(max_length = 264, blank = True)
    is_public = models.BooleanField()
    wiki = models.ForeignKey(Wiki, related_name = 'wiki', on_delete = models.DO_NOTHING, blank = True, null = True)
    projects = models.ManyToManyField(Project, related_name = 'projects', blank = True)
    repository_users = models.ManyToManyField(RepositoryUser, related_name = 'repository_users', blank = True)
    branches = models.ManyToManyField(Branch, related_name = 'branches', blank = True)