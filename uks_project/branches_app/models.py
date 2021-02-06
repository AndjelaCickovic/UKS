from django.db import models
from django.contrib import admin
from repositories_app.models import Repository


class Commit(models.Model):
    name = models.CharField(max_length=264,default=None)
    description = models.TextField(default=None)
    date = models.DateTimeField(default=None)

    def __str__(self):
        return self.name

class Branch(models.Model):

    name = models.CharField(max_length=264)
    parent_branch = models.ForeignKey('self',null=True,on_delete=models.SET_NULL)
    default = models.BooleanField(default=False)
    repository = models.ForeignKey(Repository,on_delete=models.CASCADE)
    commits = models.ManyToManyField(Commit,related_name='commits',blank=True, default=None)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'repository'], name='unique_branch_name_in_repository')
        ]

    def __str__(self):
        return self.name
