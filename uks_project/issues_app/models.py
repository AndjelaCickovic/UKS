from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Status(models.TextChoices):
    OPEN = 'OP', _('Open')
    CLOSED = 'CL', _('Close')

class Label(models.Model):
    name = models.CharField(max_length=264)
    description = models.TextField(max_length=264, blank=True)
    colour = models.CharField(max_length=7)

class Milestone(models.Model):
    name = models.CharField(max_length=264)
    dueDate = models.DateField()
    description = models.TextField(max_length=264, blank=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.OPEN)

class Issue(models.Model):
    name = models.CharField(max_length=264)
    comment = models.CharField(max_length=264, blank=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.OPEN)
    labels = models.ManyToManyField(to=Label)
    milestones = models.ForeignKey(to=Milestone, on_delete=models.DO_NOTHING)
    #0..* user(assignees)