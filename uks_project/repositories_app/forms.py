from django.forms import ModelForm
from repositories_app.models import Repository

class RepositoryForm(ModelForm):
    class Meta:
        model = Repository
        fields = ['name', 'description', 'is_public']
