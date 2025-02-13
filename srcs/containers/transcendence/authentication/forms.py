from django import forms
from .models import User
from . import models


class ModifiedProfileForm(forms.ModelForm):
    new_password = forms.CharField(max_length=64, required=False, widget=forms.TextInput(attrs={'class': 'input', 'placeholder':"", 'type':'password'}))
    new_password_repeat = forms.CharField(max_length=64, required=False, widget=forms.TextInput(attrs={'class': 'input', 'placeholder':"", 'type':'password'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super(ModifiedProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'input', 'placeholder': ''})
        self.fields['email'].widget.attrs.update({'class': 'input', 'placeholder': ''})

class LoginForm(forms.Form):
    username = forms.CharField(max_length=64, label='username', widget=forms.TextInput(attrs={'id':'Lusername'}))
    password = forms.CharField(max_length=64, label='password', widget=forms.TextInput(attrs={'id':'Password2', 'type':'password'}))

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=64, label='username', widget=forms.TextInput(attrs={'id': 'username'}))
    email = forms.CharField(max_length=300, label='mail', widget=forms.TextInput(attrs={'id': 'mail'}))
    password1 = forms.CharField(max_length=64, label='password', widget=forms.TextInput(attrs={'id': 'password', 'type': 'password'}))
    password2 = forms.CharField(max_length=64, label='password2', widget=forms.TextInput(attrs={'id': 'rpassword', 'type': 'password'}))

class UserSearchForm(forms.Form):
    query = forms.CharField(label='Search Users', max_length=100)

