from django import forms
from django.forms import ModelForm
from branches_app.models import Branch,Commit
from repositories_app.models import Repository



class BranchForm(ModelForm):

    class Meta:
        model=Branch
        fields=['name','parent_branch']

    def __init__(self, repository_id,*args, **kwargs):
        super().__init__(*args, **kwargs)
        repository = Repository.objects.get(id=repository_id)
        self.fields['parent_branch'].queryset = Branch.objects.filter(repository=repository)


class EditBranchForm(ModelForm):

    class Meta:
        model=Branch
        fields=['name']


class CommitForm(ModelForm):

    class Meta:
        model=Commit
        fields=['name','description']