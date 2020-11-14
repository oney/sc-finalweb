from django import forms
from . import models


class LoginForm(forms.Form):
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


class RegisterForm(forms.Form):
    genders = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    email = forms.CharField(
        label="Email",
        max_length=255,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
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
    name = forms.CharField(
        label="Name",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    gender = forms.ChoiceField(
        label='Gender',
        choices=genders,
        widget=forms.Select(attrs={'class': 'form-control'})
        )


class EditForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['picture', 'name', 'gender']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'})
        }


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
