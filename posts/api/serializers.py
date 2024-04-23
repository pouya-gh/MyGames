from rest_framework import serializers
from rest_framework.reverse import reverse
from posts.models import Game, Genre, GameDevRole, Comment, Rating
from django.contrib.auth.models import User


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["name", "slug"]

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["rating"]

class GameDevRoleSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = GameDevRole
        fields = ["user", "role"]

class TeamMembersField(serializers.RelatedField):
    def to_representation(self, value):
        game = value.instance
        devroles = GameDevRole.objects.filter(game=game).select_related("user").all()
        result = GameDevRoleSerializer(devroles, many=True)
        return result.data
    
class HyperlinkedGameCommentsListField(serializers.RelatedField):
    view_name = "api:game_comment_list"
    lookup_field = 'slug'

    def to_representation(self, value):
        try:
            fields = {}
            fields[self.lookup_field] = getattr(value.instance, self.lookup_field)
            return reverse(self.view_name, kwargs=fields, request=self.context["request"])
        except KeyError:
            raise Exception("request does not exist in context. ", self.__class__.__name__)
        except:
            raise Exception("unknown error. ", self.__class__.__name__)
        
class HyperlinkedGameCommentField(serializers.HyperlinkedIdentityField):
    game_lookup_field = "slug"
    comment_lookup_field = "pk"

    def to_representation(self, value):
        try:
            fields = {}
            fields[self.comment_lookup_field] = getattr(value, self.comment_lookup_field)
            fields[self.game_lookup_field] = getattr(value.game, self.game_lookup_field)
            return reverse(self.view_name, kwargs=fields, request=self.context["request"])
        except KeyError:
            raise Exception("request does not exist in context. ", self.__class__.__name__)
        except:
            raise Exception("unknown error. ", self.__class__.__name__)


class GameSerializer(serializers.ModelSerializer):
    genre = GenreSerializer()
    author = serializers.ReadOnlyField(source="author.username")
    team_members = TeamMembersField(read_only=True)
    file = serializers.FileField(max_length=None, allow_empty_file=False, use_url=True)
    average_rating = serializers.FloatField(read_only=True)
    comment_set = HyperlinkedGameCommentsListField(read_only=True)
    rate_url = serializers.HyperlinkedIdentityField(view_name="api:game_rate", lookup_field="slug")

    class Meta:
        model = Game
        fields = ["name", "slug", "average_rating", 
                  "genre", "author", "team_members", 
                  'file', 'image', "comment_set",
                  "rate_url"]
        
class GameInlineSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    genre = GenreSerializer(read_only=True)
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Game
        fields = ["url", "name", "slug", "average_rating", "author", "genre"]
        extra_kwargs = {
            'url': {'view_name': 'api:game_detail', 'lookup_field': 'slug'},
        }
        # extra_kwargs = {
        #     'url': {'view_name': 'accounts', 'lookup_field': 'account_name'},
        #     'users': {'lookup_field': 'username'}
        # }

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    game = serializers.HyperlinkedRelatedField(
        read_only=True, 
        view_name="api:game_detail", 
        lookup_field="slug")
    url = HyperlinkedGameCommentField(read_only=True, view_name="api:game_comment_detail")

    class Meta:
        model = Comment
        fields = ["url", "id", "body", "author", "game",]