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
        return '%s' % field.user.user

class IssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = ['name', 'comment', 'status', 'labels', 'milestone', 'assignees']

    def __init__(self, *args, **kwargs):
        repo = kwargs.pop('repository')
        super(IssueForm, self).__init__(*args, **kwargs)
        self.fields['labels'] = forms.ModelMultipleChoiceField(queryset = repo.labels.all(), required = False)
        self.fields['milestone'] = forms.ModelChoiceField(queryset = repo.milestones.all(), required = False)
        self.fields['assignees'] = CustomMMCF(queryset = repo.users.all(), widget = forms.CheckboxSelectMultiple, required = False)