from django import forms
from django.forms import ModelForm
from projects_app.models import Project, Column
from issues_app.models import Issue
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError

class ProjectForm(ModelForm):
    class Meta:
        model=Project
        fields=['name','description','repository']
        widgets = {'repository': forms.HiddenInput()}

    def clean(self):
        data = self.cleaned_data

        if Project.objects.filter(name=self.cleaned_data['name'],repository=self.cleaned_data['repository']).exists():
            raise ValidationError('Project with this name already exists in this repository')
        
        return data
    

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