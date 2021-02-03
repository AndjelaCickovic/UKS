from rest_framework import serializers
from repositories_app.models import Repository
from issues_app.serializers import LabelSerializer, IssueSerializer
from issues_app.models import Issue

class RepositorySerializer(serializers.ModelSerializer):
    issues = IssueSerializer(many = True)
    labels = LabelSerializer(many = True)
    class Meta:
        model = Repository
        fields = ('id', 'name', 'description', 'is_public', 'wiki', 'projects', 'issues', 'branches','labels', 'milestones', 'repository_users')