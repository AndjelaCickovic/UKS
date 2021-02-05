from django.db import models
from projects_app.models import Column
from users.models import AppUser
from django.utils.translation import gettext_lazy as _
from repositories_app.models import Repository

# Create your models here.
class Status(models.TextChoices):
    OPEN = 'Open', _('Opened')
    CLOSED = 'Closed', _('Closed')

class Label(models.Model):
    name = models.CharField(max_length=264)
    description = models.TextField(max_length=264, blank=True)
    colour = models.CharField(max_length=7)
    repository = models.ForeignKey(Repository, on_delete=models.DO_NOTHING, null=True)

class Milestone(models.Model):
    name = models.CharField(max_length=264)
    dueDate = models.DateField()
    description = models.TextField(max_length=264, blank=True)
    status = models.CharField(max_length=6, choices=Status.choices, default=Status.OPEN)
    repository = models.ForeignKey(Repository, on_delete=models.DO_NOTHING, null=True)

class Issue(models.Model):
    name = models.CharField(max_length=264)
    comment = models.CharField(max_length=264, blank=True)
    status = models.CharField(max_length=6, choices=Status.choices, default=Status.OPEN)
    labels = models.ManyToManyField(to=Label, blank=True)
    column = models.ForeignKey(Column, related_name='column', on_delete=models.DO_NOTHING, blank=True, null=True)
    milestone = models.ForeignKey(Milestone, related_name='milestone', on_delete=models.DO_NOTHING, blank=True, null=True)
    assignees = models.ManyToManyField(AppUser, related_name='assignees', blank=True)
    repository = models.ForeignKey(Repository, on_delete=models.DO_NOTHING, null=True)
