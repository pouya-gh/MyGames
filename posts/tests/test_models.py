from django.test import TestCase
from posts.models import Genre, Game, Rating, GameDevRole
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from games import settings
import shutil

class GameModelTestClass(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        print('setUpTestData: run once to set up non-modified data for all class methods.')
        User.objects.create(**{'username':"user1", 'password':"123456789)"})
        User.objects.create(**{'username':"user2", 'password':"123456789)"})
        Genre.objects.create(name="FPS", slug="fps")
        Game.objects.create(name = 'Test', slug='test', 
                            description='testsing osijfoei j',
                            author_id = 1,
                            genre_id = 1,
                            video_url = "someurl.com",
                            file = SimpleUploadedFile("best_file_eva.txt",
                                                        b"these are the file contents!"),
                            image = SimpleUploadedFile("best_fa.txt",
                                                        b"these are the file contents!"),
                            is_published = True)
        
        Game.objects.create(name = 'Test2', slug='test2', 
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
        # super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(settings.test.MEDIA_ROOT, ignore_errors=True)
        #super().tearDownClass()

    def setUp(self) -> None:
        print("setUp: run once for every test method to set up clean data.")
        pass

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
