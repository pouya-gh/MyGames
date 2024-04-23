from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path("", views.GameList.as_view(), name="home"),
    path("readme/", views.readme_page, name='readme'),
    path("games/", views.GameList.as_view(), name="game_list"),
    path("games/play/<slug:slug>", views.game_play, name='game_play'),
    path("games/edit/<slug:slug>", views.GameEdit.as_view(), name="game_edit"),
    path("games/new", views.GameCreate.as_view(), name='game_create'),
    path("games/delete/<slug:slug>", views.GameDelete.as_view(), name='game_delete'),
    path("games/<slug:slug>", views.GameDetails.as_view(), name='game_details'),
    path("games/<int:game_id>/comment/new", views.CommentCreate.as_view(), name='comment_create'),
    path("comments/<int:pk>", views.CommentDelete.as_view(), name='comment_delete'),
    path("comments/<int:pk>/edit", views.CommentUpdate.as_view(), name='comment_edit'),
    path("rating/<int:game_id>", views.rate_game, name='rate_game'),# registered with different names for convenience. one for GET and one for POST 
    path("rating/<int:game_id>", views.rate_game, name='rating_of_game'),# registered with different names for convenience. one for GET and one for POST
    path("gamedevroles/<slug:slug>", views.edit_gamedevroles, name='edit_gamedevroles'),
]
