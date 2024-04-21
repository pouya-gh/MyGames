from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.metadata import SimpleMetadata

from posts.models import Game, Rating, Comment
from .serializers import GameSerializer, GameInlineSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly

class GameListView(generics.ListAPIView):
    queryset = Game.published_games.select_related("genre", "author").all()
    serializer_class = GameInlineSerializer

class GameRetrieveView(generics.RetrieveAPIView):
    queryset = Game.published_games.select_related("genre", "author").all()
    serializer_class = GameSerializer
    lookup_field = 'slug'

# class GameViewSet(viewsets.ReadOnlyModelViewSet):
#     permission_classes = [IsAuthenticated]
#     queryset = Game.published_games.select_related("genre", "author").all()
#     serializer_class = GameSerializer
#     lookup_field = 'slug'

class GameRateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, slug, format=None):
        rating = request.data.get("rating")
        game = get_object_or_404(Game, slug=slug)
        game_rating: Rating = Rating.objects.filter(game=game, user=request.user).first()
        if game_rating:
            game_rating.rating = rating
            game_rating.save()
        else:
            game.ratings.add(rating=rating, game=game, user=request.user)
        game.average_rating = game.calculate_averate_rating()
        game.save()
        return Response({'rated': True})
    

class GameCommentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        return CommentSerializer(*args, **kwargs)

    def post(self, request, slug, format=None):
        game = get_object_or_404(Game, slug=slug)
        body = request.data.get("body")
        game.comment_set.create(body=body, author=request.user)
        return Response({'comment_posted': True})
    
    def get(self, request, slug, format=None):
        game = get_object_or_404(Game, slug=slug)
        query = game.comment_set.select_related("author").all()
        serializer = CommentSerializer(query, many=True, context={"request": request})
        return Response(serializer.data)
    
class GameCommentDetailView(APIView):
    permission_classes = [IsAuthorOrReadOnly]

    def get_serializer(self, *args, **kwargs):
        return CommentSerializer(*args, **kwargs, context={"request": self.request})

    
    def get(self, request, slug, pk, format=None):
        comment = get_object_or_404(Comment.objects.select_related("author", "game").all(), pk=pk)
        serializer = CommentSerializer(comment, context={"request": request})
        self.check_object_permissions(request, comment)
        return Response(serializer.data)

    def delete(self, request, slug, pk, format=None):
        comment = get_object_or_404(Comment.objects.select_related("author").all(), pk=pk)
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response({'comment_deleted': True})
    
    def patch(self, request, slug, pk, format=None):
        comment = get_object_or_404(Comment.objects.select_related("author").all(), pk=pk)
        body = request.data.get("body")
        self.check_object_permissions(request, comment)
        comment.body = body
        comment.save()
        return Response({'comment_updated': True})
        