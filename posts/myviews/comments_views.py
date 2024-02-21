from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..forms import CommentForm
from ..models import Game, Comment

class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'posts/comments/form.html'
    template_name_field = 'form'

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form = CommentForm(request.POST)
        game = get_object_or_404(Game, pk=kwargs["game_id"])
        print(game.name)
        if form.is_valid():
            cd = form.cleaned_data
            comment = form.save(commit=False)
            comment.game = game
            comment.author = request.user
            comment.save()
            return redirect(game)
        return render(request, 'posts/comments/form.html', {'form': form})
        
    
class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "posts/comments/form.html"
    template_name_field = 'form'

    def get_queryset(self) -> QuerySet[Any]:
        return self.model.objects.filter(author=self.request.user)
    
    def get_success_url(self) -> str:
        return self.get_object().game.get_absolute_url()
     

class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment

    def get_queryset(self) -> QuerySet[Any]:
        return self.model.objects.filter(author=self.request.user)

    def get_success_url(self) -> str:
        return self.get_object().game.get_absolute_url()