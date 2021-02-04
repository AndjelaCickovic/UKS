from rest_framework import serializers
from repositories_app.models import Repository

class RepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = ('id', 'name', 'description', 'is_public', 'wiki', 'projects', 'branches', 'repository_users')