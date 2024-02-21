from django.db import models
from django.db.models.query import QuerySet
from django.db.models import Avg
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator;
from games import settings
from .tasks import extract_gamefile
from django.urls import reverse

import shutil

class PublishedGamesManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(is_published=True)

class Genre(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)

    def __str__(self) -> str:
        return self.name

def game_file_path_maker(instance, foldername='file'):
    return 'game_{0}/{1}'.format(instance.slug, foldername) 

def game_file_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'game_{0}/{1}/{2}'.format(instance.slug, 'file', filename)

def game_image_directory_path(instance, filename):
    return 'game_{0}/{1}/{2}'.format(instance.slug, 'image', filename)

class Game(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="published_games")
    genre = models.ForeignKey(Genre, on_delete=models.DO_NOTHING)
    file = models.FileField(upload_to=game_file_directory_path, blank=False)
    image = models.ImageField(upload_to=game_image_directory_path, blank=False)
    video_url = models.URLField()
    tags = TaggableManager()

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    publish = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=False)

    average_rating = models.FloatField(default=0)

    team_members = models.ManyToManyField(User, through='GameDevRole', related_name='developed_games')
    ratings = models.ManyToManyField(User, through='Rating', related_name='rated_games')

    objects = models.Manager()
    published_games = PublishedGamesManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]

    def __str__(self) -> str:
        return self.name
    
    def calculate_averate_rating(self):
        """
        calculates average ratinge. returns 0 if there is no rating 
        """
        result = Rating.objects.filter(game=self).aggregate(Avg("rating"))
        return result['rating__avg']
    
    def save(self, *args, **kwargs):
        """
        remove the old game file and image if they were changed
        """
        should_extract_gamefiles = False
        if self.id: # the game is being updated 
            previous = Game.objects.get(pk=self.id)
            if previous.file != self.file:
                # print(f'file of {self.name} changed from {previous.file} to {self.file}')
                shutil.rmtree(settings.MEDIA_ROOT / game_file_path_maker(previous))
                # with zipfile.ZipFile(self.file, 'r') as thefile:
                #     thefile.extractall(settings.MEDIA_ROOT / game_file_path_maker(self))
                should_extract_gamefiles = True
                
            if previous.image != self.image:
                shutil.rmtree(settings.MEDIA_ROOT / game_file_path_maker(previous, 'image'))
        else:
            pass
        super(Game, self).save(*args, **kwargs)
        if should_extract_gamefiles:
            extract_gamefile.delay(str(settings.MEDIA_ROOT / game_file_path_maker(self)),
                                       str(self.file.path))
            
    def get_absolute_url(self):
        return reverse("posts:game_details", kwargs={"slug": self.slug})
    


class Rating(models.Model):
    rating = models.PositiveSmallIntegerField(default=10,
                                              validators=[
                                                  MinValueValidator(1),
                                                  MaxValueValidator(10),
                                              ])
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):
    body = models.TextField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

class GameDevRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    role = models.CharField(max_length=250)