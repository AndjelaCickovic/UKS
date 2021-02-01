from django.forms import ModelForm
from projects_app.models import Project, Column

class ProjectForm(ModelForm):
    class Meta:
        model=Project
        fields=['name','description']

class ColumnForm(ModelForm):
    class Meta:
        model = Column
        fields=['name']