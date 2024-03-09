from collections.abc import Mapping
from typing import Any
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from django.contrib.auth.forms import UserCreationForm
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

class MyUserCreationForm(UserCreationForm):
    invitation_id = forms.UUIDField(
        label = "Invitation Code", 
        help_text= "If I've sent you a résumé but no invitaion code, contact me"
        )

    class Meta:
        model = User
        fields = ("username", "invitation_id", )