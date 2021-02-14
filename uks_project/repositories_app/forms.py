from django import forms
from django.forms import ModelForm
from repositories_app.models import Repository, RepositoryUser
from users.models import AppUser
from repositories_app import views

class RepositoryForm(ModelForm):
    class Meta:
        model = Repository
        fields = ['name', 'description', 'is_public']

class CustomMCF(forms.ModelChoiceField):
    def label_from_instance(self, field):
        return '%s' % field.user

class CustomCF(forms.CharField):
    def label_from_instance(self, field):
        return '%s' % field.user

class RepositoryUserForm(ModelForm):
    class Meta:
        model = RepositoryUser
        fields = ['user', 'role']
    def __init__(self, *args, **kwargs):
        my_arg = kwargs.pop('my_arg')
        super(RepositoryUserForm, self).__init__(*args, **kwargs)
        users= CustomMCF(queryset=AppUser.objects.all().exclude(id__in=my_arg))
        self.fields['user'] = users

class EditMemberForm(ModelForm):
    class Meta:
        model = RepositoryUser
        fields = ['role']
        
