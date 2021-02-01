from django.forms import ModelForm
from issues_app.models import Label, Milestone

class LabelForm(ModelForm):
    class Meta:
        model = Label
        fields = ['name', 'description', 'colour']

class MilestoneForm(ModelForm):
    class Meta:
        model = Milestone
        fields = ['name', 'dueDate', 'description', 'status']