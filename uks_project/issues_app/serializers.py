from rest_framework import serializers
from issues_app.models import Label, Issue

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ('id', 'name', 'description', 'colour')

class IssueSerializer(serializers.ModelSerializer):
    labels = LabelSerializer(many=True)

    class Meta:
        model = Issue
        fields = ('id', 'name', 'comment', 'status', 'labels')