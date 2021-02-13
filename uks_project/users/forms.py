from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    profile_picture = forms.ImageField(required=False)


    class Meta():
        model = User
        fields = ('first_name','last_name','email','username', 'password')
        help_texts = {
            'username': None,
        }
    
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")


class EditUserForm(UserForm):

    old_password = forms.CharField(widget=forms.PasswordInput(),required=False)
    password = forms.CharField(widget=forms.PasswordInput(),label='New password',required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(),required=False)
    change_profile_picture = forms.ImageField(label='Change profile picture')

    field_order= ['first_name','last_name','email','old_password','password','confirm_password','profile_picture']

    class Meta():
        model = User
        fields = ('first_name','last_name','email')

    
        
