from django.forms import ModelForm
from issues_app.models import Label

class LabelForm(ModelForm):
    class Meta:
        model = Label
        fields = ['name', 'description', 'colour']