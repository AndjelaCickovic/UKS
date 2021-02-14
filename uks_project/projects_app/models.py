from django.db import models
from django.utils.translation import gettext_lazy as _
from repositories_app.models import Repository

class Status(models.TextChoices):
    OPEN = 'Open', _('Opened')
    CLOSED = 'Closed', _('Closed')
    
class Project(models.Model):
    name = models.CharField(max_length=264)
    description = models.TextField(max_length=264, blank=True)
    status = models.CharField(max_length=6, choices=Status.choices, default=Status.OPEN)
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name='projects',null=True)

    def __str__(self):
        return self.name
    

class Column(models.Model):
    name = models.CharField(max_length=264)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='columns')

    def __str__(self):
        return self.name