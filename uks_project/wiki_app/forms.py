from django import forms
from django.forms import ModelForm
from wiki_app.models import Page, Wiki
from django.core.exceptions import ValidationError

class PageForm(ModelForm):
    class Meta:
        model=Page
        fields=['title','content','message','wiki']
        widgets = {'wiki': forms.HiddenInput()}

    def clean(self):
        data = self.cleaned_data

        if Page.objects.filter(title=self.cleaned_data['title'],wiki=self.cleaned_data['wiki']).exists():
            raise ValidationError('Page with this name already exists in this wiki')
        
        return data   