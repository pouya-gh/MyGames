from django.test import TestCase
from django.urls import reverse
from posts.models import Genre, Game, Rating, GameDevRole
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from games import settings

import shutil

class TestPostsGamesViews(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        User.objects.create(**{'username':"user1", 'password':"123456789))"})
        User.objects.create(**{'username':"user2", 'password':"123456789)"})
        Genre.objects.create(name="FPS", slug="fps")
        Game.objects.create(name = 'very cool game', slug='very-cool-game', 
                            description='testsing osijfoei j',
                            author_id = 1,
                            genre_id = 1,
                            video_url = "someurl.com",
                            file = SimpleUploadedFile("best_file_eva.txt",
                                                        b"these are the file contents!"),
                            image = SimpleUploadedFile("best_fa.txt",
                                                        b"these are the file contents!"),
                            is_published = True)
        
        Game.objects.create(name = 'very bad game', slug='very-bad-game', 
                            description='testsing osijfoei j',
                            author_id = 1,
                            genre_id = 1,
                            video_url = "someurl.com",
                            file = SimpleUploadedFile("best_file_eva.txt",
                                                        b"these are the file contents!"),
                            image = SimpleUploadedFile("best_fa.txt",
                                                        b"these are the file contents!"),
                            is_published = True)
        
        Game.objects.create(name = 'unpublished game', slug='unpublished-game', 
                            description='testsing osijfoei j',
                            author_id = 1,
                            genre_id = 1,
                            video_url = "someurl.com",
                            file = SimpleUploadedFile("best_file_eva.txt",
                                                        b"these are the file contents!"),
                            image = SimpleUploadedFile("best_fa.txt",
                                                        b"these are the file contents!"),
                            is_published = False)
        
        GameDevRole.objects.create(game_id=1, user_id=1, role="Composer")
        super().setUpTestData()

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(settings.test.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()


    def test_games_list_view(self):
        response = self.client.get("")

        self.assertEqual(response.status_code, 200)

    def test_games_list_search_view(self):
        response = self.client.get(reverse("posts:home"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['games']), 2, "the games list doesn't contain only published games")
        self.assertTemplateUsed(response, "posts/game/list.html")

    def test_redirect_game_create_if_loggedout(self):
        response = self.client.get(reverse("posts:game_create"))

        self.assertEqual(response.status_code, 302)

    def test_games_create_get_view(self):
        login = self.client.force_login(User.objects.first())
        response = self.client.get(reverse("posts:game_create"))

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['form'])
        self.assertTemplateUsed(response, "posts/game/form.html")

    def test_games_create_empty_post_view(self):
        login = self.client.force_login(User.objects.first())
        response = self.client.post(reverse("posts:game_create"))

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['form'])
        self.assertTemplateUsed(response, "posts/game/form.html")
