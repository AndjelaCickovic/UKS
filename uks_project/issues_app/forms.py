from django import forms
from django.forms import ModelForm
from issues_app.models import Label, Milestone, Issue
from users.models import AppUser
from projects_app.models import Column

class LabelForm(ModelForm):
    class Meta:
        model = Label
        fields = ['name', 'description', 'colour']

class MilestoneForm(ModelForm):
    class Meta:
        model = Milestone
        fields = ['name', 'dueDate', 'description', 'status']

class CustomMMCF(forms.ModelMultipleChoiceField):
    def label_from_instance(self, field):
        if hasattr(field, 'name'):
            return '%s' % field.name
        else:
            return '%s' % field.user

class CustomMCF(forms.ModelChoiceField):
    def label_from_instance(self, field):
        return '%s' % field.name

class IssueForm(ModelForm):
    labels = CustomMMCF(queryset=Label.objects.all())
    #column = CustomMCF(queryset=Column.objects.all(), empty_label='None')
    #milestone = CustomMCF(queryset=Milestone.objects.all(), empty_label='None')
    assignees = CustomMMCF(queryset=AppUser.objects.all(), widget = forms.CheckboxSelectMultiple)

    class Meta:
        model = Issue
        fields = ['name', 'comment', 'status', 'labels', 'assignees']