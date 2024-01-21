from collections.abc import Mapping
from typing import Any
from django import forms
from .models import Game, Comment, Rating, GameDevRole
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# from django.core.validators import MaxValueValidator, MinValueValidator;
# from django.forms import formset_factory

class GameForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['genre'].widget.attrs.update({'class':"form-select"})
        self.fields['slug'].widget.attrs.update({'class':"form-control"})
        self.fields['description'].widget.attrs.update({'class':"form-control"})
        self.fields['file'].widget.attrs.update({'class':"form-control"})
        self.fields['image'].widget.attrs.update({'class':"form-control"})
        self.fields['video_url'].widget.attrs.update({'class':"form-control"})
        self.fields['tags'].widget.attrs.update({'class':"form-control"})
        self.fields['name'].widget.attrs.update({'class':"form-control"})

    class Meta:
        model = Game
        fields = ['name', 'slug', 'description', 'genre', 'file', 'image',
                  'video_url', 'tags', 'is_published']
        
class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['body'].widget.attrs.update({'class':"form-control"})
        self.fields['body'].label = False

    class Meta:
        model = Comment
        fields = ['body']

class RatingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['rating'].widget.attrs.update(
            {'max':10, 'min':1, 'class':"form-control"})
        self.fields['rating'].label = False

    class Meta:
        model = Rating
        fields = ['rating']

    def clean_rating(self):
        r = self.cleaned_data['rating']
        if r > 10:
            r = 10

        return r

class GameDevRoleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        myInstance = kwargs.get('instance')
        myInitial = kwargs.get('initial')
        if  (myInstance is not None):
            if myInitial is None:
                myInitial = {}
            # print(self.fields['dev_username'])
            myInitial.update({'dev_username': myInstance.user.username})
        super().__init__(initial=myInitial, *args, **kwargs)
        self.fields['role'].widget.attrs.update({'class':"form-control"})
        self.fields['dev_username'].widget.attrs.update({'class':"form-control"})
        
        
        # self.fields['game'].widget.attrs.update(type='hidden')
    dev_username = forms.CharField(max_length=250, label="Developer's username")
    field_order = ['dev_username', 'role']

    class Meta:
        model = GameDevRole
        fields = ['role']
        # widgets = {'game': forms.HiddenInput()}

    def clean_dev_username(self):
        username = self.cleaned_data.get('dev_username')
        if not User.objects.filter(username=username).exclude():
            raise ValidationError("developer's username does not exit", code='invalid dev username')
        return username
    
    def save(self, commit: bool = ...) -> Any:
        obj = super().save(commit = False)
        dev = User.objects.get(username=self.cleaned_data.get('dev_username'))
        obj.user = dev
        if commit:
            obj.save()
        return obj

# GameDevRoleFormset = formset_factory(GameDevRoleForm)
# class MyForm(forms.Form):
#     rating = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])