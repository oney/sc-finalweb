from django import forms
from .. import models


class EditForm(forms.ModelForm):
    '''
    The form for /edit page
    '''
    picture = forms.ImageField(required=False)

    class Meta:
        model = models.User
        fields = ['picture', 'name', 'gender']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'})
        }
