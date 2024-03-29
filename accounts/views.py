from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST 
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from .models import Profile
from django.contrib.auth.models import User, Group

from .models import Profile
from .forms import UserUpdateForm, ProfileForm

def sign_up(request):
    if request.user.is_authenticated:
        return redirect("posts:game_list")

    user_creation_form = UserCreationForm(request.POST or None)

    if request.POST:
        if user_creation_form.is_valid():
            cd = user_creation_form.cleaned_data
            new_user = user_creation_form.save()
            new_user.profile = Profile.objects.create(user_id=new_user.id, bio="")
            default_group = Group.objects.get(name="NormalUsers")
            new_user.groups.add(default_group)
            new_user.save()
            user = authenticate(username=cd['username'], password=cd['password1'])
            login(request, user)
            return redirect("posts:game_list")

            
    return render(request, "registration/signup.html", {'form': user_creation_form})

def profile_details(request, username):
    user = get_object_or_404(User, username=username)
    published_games = user.published_games.all()
    developed_games = user.developed_games.all().distinct()
    return render(request, "registration/profile.html", 
                  {'user': user,
                   'published_games': published_games,
                   'developed_games': developed_games,})

@login_required
def profile_update(request):
    user_form = UserUpdateForm(request.POST or None, instance=request.user)
    if request.user.profile is None:
        profile_form = ProfileForm(request.POST or None)
    else:
        profile_form = ProfileForm(request.POST or None, instance=request.user.profile)
    
    if request.POST:
        if user_form.is_valid() and profile_form.is_valid():
            cd = user_form.cleaned_data
            cdd = profile_form.cleaned_data
            user_form.save()

            new_profile = profile_form.save(commit=False)
            if not new_profile.user_id:
                new_profile.user_id = request.user.id
            new_profile.save()

            return redirect("accounts:profile_details", username=request.user.username)
    
    return render(request, 'registration/profile_form.html', 
                  {'user_form': user_form, 'profile_form': profile_form})