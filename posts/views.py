from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory

from .forms import GameForm, RatingForm, GameDevRoleForm, CommentForm
from .myviews.comments_views import *
from .myviews.ratings_views import *
from .models import Game, Rating, GameDevRole, game_file_path_maker

from games import settings

import os

def game_details(request, slug):
    game = get_object_or_404(Game, slug=slug)
    comments = game.comment_set.all()
    comment_form = CommentForm()
    if request.user.is_authenticated:
        try:
            rating = Rating.objects.get(game__id=game.id, user__id=request.user.id)
            rating_form = RatingForm(instance=rating)
        except ObjectDoesNotExist:
            rating_form = RatingForm()
    else:
        rating_form = None
            
    developers = GameDevRole.objects.filter(game=game)

    return render(request, 
                  "posts/game/details.html", 
                  {"game": game,
                   'comments': comments,
                   'rating_form': rating_form,
                   'developers': developers,
                   'comment_form': comment_form,})


def game_list(request):
    search_query = request.GET.get('q')
    if search_query:
        games = Game.published_games.filter(name__contains=search_query)
    else:
        games = Game.published_games.all()

    return render(request, "posts/game/list.html", {'games': games})

@login_required
def game_edit(request, slug):
    game = get_object_or_404(Game, slug=slug, author__id=request.user.id)
    if request.POST:
        form = GameForm(data=request.POST, files=request.FILES, instance=game)
        if form.is_valid():
            cd = form.cleaned_data
            game_edit = form.save()

            # return render(request, 'posts/game/details.html', {'game': game_edit})
            return redirect("posts:game_details", slug=game.slug)
        else:
            return render(request, "posts/game/form.html", {"form": form})
    else:
        form = GameForm(instance=game)
        return render(request, "posts/game/form.html", {"form": form})


@login_required
def game_create(request):
    if request.POST:
        form = GameForm(request.POST, files=request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            game = form.save(commit=False)
            game.author = request.user
            game.save()

            GameDevRole.objects.create(user=request.user, role="Original Poster", game=game)
            # game.team_members.add(user=request.user, role="Original Poster")
            # return render(request, 'posts/game/details.html', {'game': game})
            return redirect("posts:game_details", slug=game.slug)
        else:
            return render(request, "posts/game/form.html", {"form": form})
    else:
        form = GameForm()
        return render(request, "posts/game/form.html", {"form": form})

@require_POST   
@login_required
def game_delete(request, slug):
    # if request.POST:
    game = get_object_or_404(Game, slug=slug, author__id=request.user.id)
    game.delete()

    return redirect("posts:game_list")

@login_required
def edit_gamedevroles(request, slug):
    game: Game = get_object_or_404(Game, slug=slug, author=request.user)
    # devroles: GameDevRole = GameDevRole.objects.filter(game = game).all()
    DevRolesFormset = modelformset_factory(GameDevRole, 
                                           form=GameDevRoleForm, 
                                           extra=2,
                                           can_delete=True)
                                           

    formset = DevRolesFormset(request.POST or None)
    formset.queryset = queryset=GameDevRole.objects.filter(game_id=game.id)

    if request.POST:
        if formset.is_valid():
            print("slfjweo ifjowei fjeoi")
            formset.save(commit=False)
            # for obj in formset.deleted_objects:
            #     obj.delete()
            for new_obj in formset.new_objects:
                new_obj.game_id = game.id
            formset.save()
            return redirect ("posts:game_details", slug=slug)
        
    return render(request, "posts/game/gamedevroles.html", {"formset": formset, "game": game})

def game_play(request, slug):
    game = get_object_or_404(Game, slug=slug)

    game_data_folder = game_file_path_maker(game, "file") + "/" + "Build"
    game_data_root = os.path.join( settings.MEDIA_ROOT, game_file_path_maker(game, "file"), "Build")
    game_datafile_name = os.listdir(game_data_root)[0].split(".")[0]

    build_path = "/" + settings.MEDIA_URL + "/" + game_data_folder

    return render(request, "posts/game/play.html", {
        "game": game,
        "build_path": build_path,
        'data_name': game_datafile_name,
    })