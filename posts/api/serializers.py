from rest_framework import serializers
from posts.models import Game, Genre, GameDevRole
from django.contrib.auth.models import User

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["name", "slug"]

class UsernameField(serializers.RelatedField):
    def to_representation(self, value):
        return value.username

class GameDevRoleSerializer(serializers.ModelSerializer):
    user = UsernameField(read_only=True)

    class Meta:
        model = GameDevRole
        fields = ["user", "role"]

class TeamMembersField(serializers.RelatedField):
    def to_representation(self, value):
        game = value.instance
        devroles = GameDevRole.objects.filter(game=game).select_related("user").all()
        result = GameDevRoleSerializer(devroles, many=True)
        return result.data

class GameSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True)
    author = UsernameField(read_only=True)
    team_members = TeamMembersField(read_only=True)

    class Meta:
        model = Game
        fields = ["name", "slug", "average_rating", 
                  "genre", "author", "team_members"]
        
class GameInlineSerializer(serializers.ModelSerializer):
    author = UsernameField(read_only=True)
    genre = GenreSerializer(read_only=True)

    class Meta:
        model = Game
        fields = ["name", "slug", "average_rating", "author", "genre"]