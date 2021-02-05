from django import forms
from django.forms import ModelForm
from branches_app.models import Branch
from repositories_app.models import Repository



class BranchForm(ModelForm):

    name = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control' , 'autocomplete': 'off','pattern':'[A-Za-z]+', 'title':'Enter characters only '}))

    class Meta:
        model=Branch
        fields=['parent_branch']

    field_order = ['name','parent_branch']

    def __init__(self, repository_id,*args, **kwargs):
        super().__init__(*args, **kwargs)
        repository = Repository.objects.get(id=repository_id)
        self.fields['parent_branch'].queryset = Branch.objects.filter(repository=repository)
