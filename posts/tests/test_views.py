from django.test import TestCase
from django.urls import reverse
from posts.models import Genre, Game, Rating, GameDevRole
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.conf import settings

import shutil

class TestPostsGamesViews(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        image_bytes = None
        file_bytes = None
        with open("media/1x1.png", "rb") as image:
            image_bytes = image.read()
        with open('media/test.zip', 'rb') as file:
            file_bytes = file.read()
        User.objects.create(**{'username':"user1", 'password':"123456789))"})
        User.objects.create(**{'username':"user2", 'password':"123456789)"})
        Genre.objects.create(name="FPS", slug="fps")
        Genre.objects.create(name='RPG', slug='rpg')
        game1 = Game.objects.create(name = 'very cool game', slug='very-cool-game', 
                            description='testsing osijfoei j',
                            author_id = 1,
                            genre_id = 1,
                            video_url = "someurl.com",
                            file = SimpleUploadedFile("test.zip",
                                                        file_bytes),
                            image = SimpleUploadedFile("1x1.png",
                                                        image_bytes),
                            is_published = True)
        game1.tags.add("tag1")
        
        game2 = Game.objects.create(name = 'very bad game', slug='very-bad-game', 
                            description='testsing osijfoei j',
                            author_id = 1,
                            genre_id = 2,
                            video_url = "someurl.com",
                            file = SimpleUploadedFile("test.zip",
                                                        file_bytes),
                            image = SimpleUploadedFile("1x1.png",
                                                        image_bytes),
                            is_published = True)
        game2.tags.add("tag2")
        
        game3 = Game.objects.create(name = 'unpublished game', slug='unpublished-game', 
                            description='testsing osijfoei j',
                            author_id = 1,
                            genre_id = 1,
                            video_url = "someurl.com",
                            file = SimpleUploadedFile("test.zip",
                                                        file_bytes),
                            image = SimpleUploadedFile("1x1.png",
                                                        image_bytes),
                            is_published = False)
        game3.tags.add("tag3")
        
        GameDevRole.objects.create(game_id=1, user_id=1, role="Composer")
        super().setUpTestData()

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()


    def test_games_list_view(self):
        response = self.client.get("")

        self.assertEqual(response.status_code, 200)

    def test_games_list_search_view(self):
        response = self.client.get(reverse("posts:home"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['games']), 2, "the games list doesn't contain only published games")
        self.assertTemplateUsed(response, "posts/game/list.html")

    def test_games_list_search_with_tags(self):
        response = self.client.get(reverse("posts:home") + "?tag=tag1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['games']), 1)
        self.assertTemplateUsed(response, "posts/game/list.html")

    def test_games_list_search_with_tags_only_published_games(self):
        response = self.client.get(reverse("posts:home") + "?tag=tag3")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['games']), 0)
        self.assertTemplateUsed(response, "posts/game/list.html")

    def test_games_list_search_with_genre(self):
        response = self.client.get(reverse("posts:home") + "?genre=fps")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['games']), 1) #this also asserts if the search is done only in published games
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

    def test_games_create_view_post_with_valid_data(self):
        login = self.client.force_login(User.objects.first())
        
        self.assertEqual(Game.published_games.count(), 2)

        #this should work as long as the tests are run from the main folder, where manage.py is.
        image_bytes = None
        file_bytes = None
        with open("media/1x1.png", "rb") as image:
            image_bytes = image.read()
        with open('media/test.zip', 'rb') as file:
            file_bytes = file.read()
        response = self.client.post(reverse("posts:game_create"), data={
            "name": 'some game',
            "slug": 'some-game',
            "description": 'testsing osijfoei j',
            "author": 1,
            "genre": 1,
            "video_url": "someurl.com",
            "file": SimpleUploadedFile("test.zip",
                                        file_bytes),
            "image": SimpleUploadedFile("best_fa.png",
                                        image_bytes, content_type='image/png'),
            "tags": "tag1",
            "is_published": True,
        })
        self.assertEqual(Game.published_games.count(), 3)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(True)