from django import forms
from .. import models


class LoginForm(forms.Form):
    '''
    The form for /login page
    '''
    email = forms.CharField(
        label="Email",
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )
    password = forms.CharField(
        label="Password",
        max_length=255,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
        )