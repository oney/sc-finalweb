from django import forms
from .. import models


class PasswordForm(forms.Form):
    password = forms.CharField(
        label="Password",
        max_length=200,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        max_length=200,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
