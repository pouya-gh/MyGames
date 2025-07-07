from django.test import TestCase
from posts.models import Genre, Game, Rating, GameDevRole, game_file_directory_path, game_image_directory_path
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.conf import settings
import shutil

class GameModelTestClass(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        # print('setUpTestData: run once to set up non-modified data for all class methods. sdfsdf')
        image_bytes = None
        file_bytes = None
        with open("media/1x1.png", "rb") as image:
            image_bytes = image.read()
        with open('media/test.zip', 'rb') as file:
            file_bytes = file.read()
        user1 = User.objects.create(**{'username':"user1", 'password':"123456789)"})
        user2 = User.objects.create(**{'username':"user2", 'password':"123456789)"})
        Genre.objects.create(name="FPS", slug="fps")
        game1 = Game.objects.create(name = 'Test', slug='test', 
                            description='testsing osijfoei j',
                            author_id = 1,
                            genre_id = 1,
                            video_url = "someurl.com",
                            file = SimpleUploadedFile("test.zip",
                                                        file_bytes),
                            image = SimpleUploadedFile("1x1.png",
                                                        image_bytes),
                            is_published = True)
        
        game2 = Game.objects.create(name = 'Test2', slug='test2', 
                            description='testsing osijfoei j',
                            author_id = 1,
                            genre_id = 1,
                            video_url = "someurl.com",
                            file = SimpleUploadedFile("test.zip",
                                                        file_bytes),
                            image = SimpleUploadedFile("1x1.png",
                                                        image_bytes),
                            is_published = False)
        
        GameDevRole.objects.create(game_id=1, user_id=1, role="Composer")
        Rating.objects.create(rating=6, user=user1, game=game1)
        Rating.objects.create(rating=7, user=user2, game=game1)
        super().setUpTestData()

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_genre_exits(self):
        obj = Genre.objects.first()
        self.assertEqual(obj.name, "FPS")

    def test_game_exits(self):
        obj = Game.published_games.first()
        self.assertEqual(obj.name, "Test")

    def test_published_games_manager(self):
        games = Game.published_games.all()
        self.assertEqual(len(games), 1)

    def test_game_name_max_length(self):
        game = Game.objects.get(id=1)
        max_length = game._meta.get_field('name').max_length
        self.assertEqual(max_length, 250)

    def test_game_slug_max_length(self):
        game = Game.objects.get(id=1)
        max_length = game._meta.get_field('slug').max_length
        self.assertEqual(max_length, 250)

    def test_devrole_rolename_length(self):
        devrole = GameDevRole.objects.first()
        max_length = devrole._meta.get_field('role').max_length
        self.assertEqual(max_length, 250)

    def test_game_rating_range_max(self):
        obj = Rating.objects.create(rating=11, game_id=1, user_id=1)
        self.assertRaises(ValidationError, obj.full_clean)

    def test_game_rating_range_min(self):
        obj = Rating.objects.create(rating=0, game_id=1, user_id=1)
        self.assertRaises(ValidationError, obj.full_clean)

    def test_genre_name_length(self):
        genre = Genre.objects.first()
        max_length = genre._meta.get_field('name').max_length
        self.assertEqual(max_length, 250)

    def test_genre_slug_length(self):
        genre = Genre.objects.first()
        max_length = genre._meta.get_field('slug').max_length
        self.assertEqual(max_length, 250)

    def test_game_absolute_url(self):
        game: Game = Game.published_games.first()
        self.assertEqual(game.get_absolute_url(), "/games/test")

    def test_game_average_rating(self):
        game: Game = Game.published_games.first()
        self.assertAlmostEqual(game.calculate_averate_rating(), 6.5)

    def test_game_file_path_helper_functions(self):
        game: Game = Game.published_games.first()

        self.assertEqual(game.file_path_maker(), f"game_{game.slug}/file")
        self.assertEqual(game.file_path_maker("thefolder"), f"game_{game.slug}/thefolder")

        self.assertEqual(game_file_directory_path(game, "filename"), f'game_{game.slug}/file/filename')
        
        self.assertEqual(game_image_directory_path(game, "imagename"), f'game_{game.slug}/image/imagename')