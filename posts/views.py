from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.urls import reverse_lazy

from taggit.models import Tag

from .forms import GameForm, RatingForm, GameDevRoleForm, CommentForm
from .myviews.comments_views import *
from .myviews.ratings_views import *
from .models import Game, Genre, Rating, GameDevRole, game_file_path_maker

from django.conf import settings

import os

class GameDetails(DetailView):
    model = Game
    template_name = "posts/game/details.html"
    context_object_name = 'game'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        game = get_object_or_404(self.model, slug=slug)
        comments = game.comment_set.all()
        comment_form = CommentForm()
        developers = GameDevRole.objects.filter(game=game)
        tags = game.tags.all()
        if self.request.user.is_authenticated:
            try:
                rating = Rating.objects.get(game__id=game.id, user__id=self.request.user.id)
                rating_form = RatingForm(instance=rating)
            except ObjectDoesNotExist:
                rating_form = RatingForm()
        else:
            rating_form = None

        context["comments"] = comments
        context["comment_form"] = comment_form
        context["developers"] = developers
        context["rating_form"] = rating_form
        context["tags"] = tags
        return context
    

class GameList(ListView):
    model = Game
    template_name = "posts/game/list.html"
    context_object_name = "games"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        genres = Genre.objects.all()
        context['genres'] = genres
        return context

    def get_queryset(self) -> QuerySet[Any]:
        search_query = self.request.GET.get('q', '')
        tag_slug = self.request.GET.get('tag', '')
        genre_slug = self.request.GET.get('genre', '')
        if search_query:
            return self.model.published_games.filter(name__contains=search_query)
        elif tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            return self.model.published_games.filter(tags__in=[tag])
        elif genre_slug:
            genre = get_object_or_404(Genre, slug=genre_slug)
            return self.model.published_games.filter(genre=genre)
        else:
            return self.model.published_games.all()

class GameCreate(LoginRequiredMixin, CreateView):
    model = Game
    form_class = GameForm
    context_object_name = 'game'
    template_name = "posts/game/form.html"
    template_name_field = 'form'

    def form_valid(self, form):
        # form.cleaned_data
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        GameDevRole.objects.create(user=self.request.user, role="Original Poster", game=self.object)

        return redirect(self.object)
    
class GameEdit(LoginRequiredMixin, UpdateView):
    model = Game
    form_class = GameForm
    context_object_name = 'game'
    template_name = "posts/game/form.html"
    template_name_field = 'form'

class GameDelete(LoginRequiredMixin, DeleteView):
    model = Game
    success_url = reverse_lazy("posts:game_list")
    def get_queryset(self):
        return self.model.objects.filter(slug=self.kwargs.get('slug', ''), author=self.request.user)

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