from rest_framework import generics
from posts.models import Game
from .serializers import GameSerializer, GameInlineSerializer

class GameListView(generics.ListAPIView):
    queryset = Game.published_games.select_related("genre", "author").all()
    serializer_class = GameInlineSerializer

class GameRetrieveView(generics.RetrieveAPIView):
    queryset = Game.published_games.select_related("genre", "author").all()
    serializer_class = GameSerializer
    lookup_field = 'slug'