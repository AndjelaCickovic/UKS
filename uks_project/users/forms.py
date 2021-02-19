from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError

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
            raise ValidationError({'confirm_password':["Passwords do not match."]})

class EditUserForm(UserForm):

    old_password = forms.CharField(widget=forms.PasswordInput(),required=False)
    password = forms.CharField(widget=forms.PasswordInput(),label='New password',required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(),required=False)
    profile_picture = forms.ImageField(label='Change profile picture',required=False)

    field_order= ['first_name','last_name','email','old_password','password','confirm_password']

    def clean(self):

        if(self.is_valid()):
            old_password = self.cleaned_data['old_password']
            new_password = self.cleaned_data['password']
            confirm_password = self.cleaned_data['confirm_password']

            user = User.objects.get(username=self.instance.username)

            if old_password:
                if user.check_password(old_password):                    
                    if not new_password:
                        raise ValidationError({'password':['Invalid value for new password submitted.']})
                    else:
                        if new_password != confirm_password:
                            raise ValidationError({'confirm_password':["Passwords do not match."]})
                else:
                    raise ValidationError({'old_password':['Old password is not correct.']})
            else:
                if new_password:
                    raise ValidationError ({'old_password':['Please submit value for old password.']})

    class Meta():
        model = User
        fields = ('first_name','last_name','email')

    
        
