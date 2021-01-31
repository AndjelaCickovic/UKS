from django.db import models
from projects_app.models import Column
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Status(models.TextChoices):
    OPEN = 'Open', _('Opened')
    CLOSED = 'Closed', _('Closed')

class Label(models.Model):
    name = models.CharField(max_length=264)
    description = models.TextField(max_length=264, blank=True)
    colour = models.CharField(max_length=7)

class Milestone(models.Model):
    name = models.CharField(max_length=264)
    dueDate = models.DateField()
    description = models.TextField(max_length=264, blank=True)
    status = models.CharField(max_length=6, choices=Status.choices, default=Status.OPEN)

class Issue(models.Model):
    name = models.CharField(max_length=264)
    comment = models.CharField(max_length=264, blank=True)
    status = models.CharField(max_length=6, choices=Status.choices, default=Status.OPEN)
    labels = models.ManyToManyField(to=Label, blank=True)
    column = models.ForeignKey(Column, on_delete=models.CASCADE, blank=True, null=True)
    #milestones = models.ForeignKey(to=Milestone, on_delete=models.DO_NOTHING, blank=True, null=True)
    #0..* user(assignees)