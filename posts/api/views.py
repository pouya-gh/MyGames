from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.reverse import reverse
from django.shortcuts import get_object_or_404

from posts.models import Game, Rating, Comment
from .serializers import GameSerializer, GameInlineSerializer, CommentSerializer, RatingSerializer
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

    def get_serializer(self, *args, **kwargs):
        return RatingSerializer(*args, **kwargs, context={"request": self.request})

    def post(self, request, slug, format=None):
        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            rating = serializer.validated_data["rating"]#.get("rating")
            game = get_object_or_404(Game, slug=slug)
            self.check_object_permissions(request, game)
            game_rating: Rating = Rating.objects.filter(game=game, user=request.user).first()
            if game_rating:
                game_rating.rating = rating
                game_rating.save()
            else:
                game.ratings.add(rating=rating, game=game, user=request.user)
            game.average_rating = game.calculate_averate_rating()
            game.save()
            return Response({'rated': True})
        else:
            return Response({'rated': False})
    

class GameCommentListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    queryset = Game.published_games.all()

    # def get_serializer(self, *args, **kwargs):
    #     return CommentSerializer(*args, **kwargs)

    def post(self, request, slug, format=None):
        game = get_object_or_404(self.get_queryset(), slug=slug)
        body = request.data.get("body")
        game.comment_set.create(body=body, author=request.user)
        return Response({'comment_posted': True})
    
    def get(self, request, slug, format=None):
        game = get_object_or_404(self.get_queryset(), slug=slug)
        query = game.comment_set.select_related("author").all()
        serializer = CommentSerializer(query, many=True, context={"request": request})
        return Response(serializer.data)
    
class GameCommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    
    def get(self, request, slug, pk, format=None):
        comment = get_object_or_404(self.get_queryset().select_related("author", "game").all(), pk=pk)
        serializer = CommentSerializer(comment, context={"request": request})
        self.check_object_permissions(request, comment)
        return Response(serializer.data)

    def delete(self, request, slug, pk, format=None):
        comment = get_object_or_404(self.get_queryset().select_related("author").all(), pk=pk)
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response({'comment_deleted': True})
    
    def put(self, request, slug, pk, format=None):
        comment = get_object_or_404(self.get_queryset().select_related("author").all(), pk=pk)
        body = request.data.get("body")
        self.check_object_permissions(request, comment)
        comment.body = body
        comment.save()
        return Response({'comment_updated': True})
        
@api_view(['GET'])
@permission_classes([])
def api_root(request, format=None):
    return Response({
        "login": reverse("rest_login", request=request, format=format),
        "logout": reverse("rest_logout", request=request, format=format),
        "games": reverse("api:game_list", request=request, format=format),
        "schema": reverse("api:schema", request=request, format=format),
        "swagger_docs": reverse("api:swagger_docs", request=request, format=format),
    })