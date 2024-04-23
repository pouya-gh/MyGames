from django.urls import path
from posts.api.views import (
    GameRateView, GameListView, 
    GameRetrieveView, GameCommentListView,
    GameCommentDetailView, api_root)
from rest_framework.routers import SimpleRouter

# router = SimpleRouter()
# router.register("games", GameViewSet, basename="games")

app_name = "api"

urlpatterns = [
    path("", api_root, name="api_root"),
    path("games/",
         GameListView.as_view(),
        name="game_list"),
    path("games/<slug:slug>",
         GameRetrieveView.as_view(),
         name="game_detail"),
    path("games/<slug:slug>/rate",
         GameRateView.as_view(),
         name='game_rate'),
     path("games/<slug:slug>/comments/",
          GameCommentListView.as_view(),
          name="game_comment_list"),
     path("games/<slug>/comments/<pk>",
          GameCommentDetailView.as_view(),
          name="game_comment_detail"),
]
# urlpatterns += router.urls
