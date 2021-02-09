from django import forms
from django.forms import ModelForm
from projects_app.models import Project, Column
from issues_app.models import Issue

class ProjectForm(ModelForm):
    class Meta:
        model=Project
        fields=['name','description']

class ColumnForm(ModelForm):
    class Meta:
        model = Column
        fields=['name']

class CustomMCF(forms.ModelChoiceField):
    def column_from_instance(self, field):
        return '%s' % field.name

class IssueColumnForm(ModelForm):
    columns = CustomMCF(queryset = Column.objects.all())

    class Meta:
        model = Issue
        fields = ['columns']