from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

# from ..views import *
from ..forms import RatingForm
from ..models import Game, Rating

@login_required
def rate_game(request, game_id):
    """
    i tried to mix 2 views in one function here, like most "create" views. 
    i register this function in urls twice with different names. one for
    the GET part and the other for the POST part.
    """
    if request.POST:
        rating_form = RatingForm(request.POST)
        game = Game.objects.get(pk=game_id)
        if rating_form.is_valid():
            cd = rating_form.cleaned_data
            (r, _) = Rating.objects.get_or_create(game=game, user=request.user)
            r.rating = cd['rating']
            r.save()
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