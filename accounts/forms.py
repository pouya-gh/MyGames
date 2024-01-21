from collections.abc import Mapping
from typing import Any
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Profile
from django.contrib.auth.models import User

class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['date_of_birth'].widget.attrs.update({'class':"form-control"})
        self.fields['bio'].widget.attrs.update({'class':"form-control"})
        
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'bio']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})
        }

class UserUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class':"form-control"})
        self.fields['last_name'].widget.attrs.update({'class':"form-control"})
        self.fields['email'].widget.attrs.update({'class':"form-control"})

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']