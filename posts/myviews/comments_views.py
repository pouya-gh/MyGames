from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

# from ..views import *
from ..forms import CommentForm
from ..models import Game, Comment

@login_required
def comment_create(request, game_id):
    game = get_object_or_404(Game, pk=game_id)

    if request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            comment = form.save(commit=False)
            comment.game = game
            comment.author = request.user
            comment.save()

            return redirect("posts:game_details", slug=game.slug)
        else:
            return render(request, 'posts/comments/form.html', {'form': form})
    else:
        form = CommentForm()

        return render(request, 'posts/comments/form.html', {'form': form})
    
@login_required
def comment_edit(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, author__id=request.user.id)
    
    if request.POST:
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            cd = form.cleaned_data
            form.save()

            return redirect("posts:game_details", slug=comment.game.slug)
        else:
            return render(request, 'posts/comments/form.html', {'form': form})
    else:
        form = CommentForm(instance=comment)
        return render(request, "posts/comments/form.html", {'form': form})
    
@require_POST
@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, author__id=request.user.id)
    game = comment.game
    comment.delete()
    return redirect("posts:game_details", slug=game.slug)