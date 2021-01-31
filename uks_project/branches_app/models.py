from django.db import models

class Branch(models.Model):
    name = models.CharField(max_length=264)
    parent_branch = models.ForeignKey('self', null=True, on_delete=models.DO_NOTHING)

class Commit(models.Model):
    name = models.CharField(max_length=264)
    description = models.TextField()
    date = models.DateTimeField()
    branch = models.ForeignKey(Branch, related_name='commits', on_delete=models.DO_NOTHING)