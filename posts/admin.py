from django.contrib import admin
from .models import Genre, Game, Comment, GameDevRole, Rating, SiteVisitTracker

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

class GenreInline(admin.StackedInline):
    model = Genre

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'genre', 'created']
    list_filter = ['created', 'genre', 'author']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ['author']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['game', 'author', 'body']
    list_filter = ['game', 'created']
    search_fields = ['game', 'author', 'body']

    raw_id_fields = ['game', 'author']

@admin.register(GameDevRole)
class GameDevRolesAdmin(admin.ModelAdmin):
    list_display = ['user', 'game', 'role']
    list_filter = ['user', 'game', 'role']
    search_fields = ['user', 'game', 'role']

    raw_id_fields = ['user', 'game']

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['game', 'user', 'rating']

@admin.register(SiteVisitTracker)
class SiteVisitTrackersAdmin(admin.ModelAdmin):
    list_display = ['ip', 'visit_time', 'visit_counter']
    list_filter = ['ip', 'visit_time']