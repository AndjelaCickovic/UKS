from rest_framework import serializers
from issues_app.models import Label, Issue, Milestone
from projects_app.models import Column
from users.models import AppUser

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ('id', 'name', 'description', 'colour')

class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ('id', 'name')

class MilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milestone
        fields = ('id', 'name', 'dueDate', 'description', 'status')

class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ('id', 'user')

class IssueSerializer(serializers.ModelSerializer):
    labels = LabelSerializer(many=True)
    column = ColumnSerializer()
    milestone = MilestoneSerializer()
    assignees = AppUserSerializer(many=True)

    class Meta:
        model = Issue
        fields = ('id', 'name', 'comment', 'status', 'labels', 'column', 'milestone', 'assignees')