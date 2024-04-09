from django.urls import path
from posts.api.views import GameListView, GameRetrieveView

app_name = 'courses'

urlpatterns = [
    path("games/",
         GameListView.as_view(),
        name="game_list"),
    path("games/<slug:slug>",
         GameRetrieveView.as_view(),
         name="game_detail"),
]