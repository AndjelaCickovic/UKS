from django.forms import ModelForm
from wiki_app.models import Page

class PageForm(ModelForm):
    class Meta:
        model=Page
        fields=['title','content','message']