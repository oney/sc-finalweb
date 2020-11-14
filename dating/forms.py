from django import forms


class UserForm(forms.Form):
    email = forms.CharField(label="Email", max_length=255)
    password = forms.CharField(label="Password", max_length=255, widget=forms.PasswordInput)