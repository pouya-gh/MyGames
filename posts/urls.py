from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path("", views.game_list, name="home"),
    path("games/", views.game_list, name="game_list"),
    path("games/play/<slug:slug>", views.game_play, name='game_play'),
    path("games/edit/<slug:slug>", views.game_edit, name="game_edit"),
    path("games/new", views.game_create, name='game_create'),
    path("games/delete/<slug:slug>", views.game_delete, name='game_delete'),
    path("games/<slug:slug>", views.game_details, name='game_details'),
    path("games/<int:game_id>/comment/new", views.CommentCreate.as_view(), name='comment_create'),
    path("comments/<int:pk>", views.CommentDelete.as_view(), name='comment_delete'),
    path("comments/<int:pk>/edit", views.CommentUpdate.as_view(), name='comment_edit'),
    path("rating/<int:game_id>", views.rate_game, name='rate_game'),
    path("rating/<int:game_id>", views.rate_game, name='rating_of_game'),
    path("gamedevroles/<slug:slug>", views.edit_gamedevroles, name='edit_gamedevroles'),
]
