from django.forms import ModelForm
from projects_app.models import Project

class ProjectForm(ModelForm):
    class Meta:
        model=Project
        fields=['name','description']