from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

# from ..views import *
from ..forms import RatingForm
from ..models import Game, Rating

@login_required
def rate_game(request, game_id):
    if request.POST:
        rating_form = RatingForm(request.POST)
        game = Game.objects.get(pk=game_id)
        if rating_form.is_valid():
            cd = rating_form.cleaned_data
            #rating = rating_form.save(commit=False)
            (r, _) = Rating.objects.get_or_create(game=game, user=request.user)
            r.rating = cd['rating']
            # rating.game = game
            # rating.user = request.user
            # rating.save()
            r.save()
            # game.ratings.add(rating)
            game.average_rating = game.calculate_averate_rating()
            game.save()
            return JsonResponse({'msg': 'success'})
        else:
            return JsonResponse({"msg": "error"})
    else:
        try:
            rating = Rating.objects.get(game__id=game_id, user__id=request.user.id)
            return JsonResponse({'rating': str(rating.rating)})
        except ObjectDoesNotExist:
            return JsonResponse({'rating': str(10)})