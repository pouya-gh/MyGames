from django.test import TestCase
from posts.forms import GameForm, CommentForm, RatingForm, GameDevRoleForm
from django.core.files.uploadedfile import SimpleUploadedFile
from posts.models import Genre, Game, Rating, GameDevRole
from games import settings
from django.contrib.auth.models import User
import shutil

class FormsTestClass(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        # print('setUpTestData for forms data')
        image_bytes = None
        file_bytes = None
        with open("media/1x1.png", "rb") as image:
            image_bytes = image.read()
        with open('media/test.zip', 'rb') as file:
            file_bytes = file.read()
        User.objects.create(**{'username':"user3", 'password':"123456789)"})
        Genre.objects.create(name="FPS", slug="fps")
        Game.objects.create(name = 'Test3', slug='test3', 
                            description='testsing osijfoei j',
                            author_id = 1,
                            genre_id = 1,
                            video_url = "someurl.com",
                            file = SimpleUploadedFile("test.zip",
                                                        file_bytes),
                            image = SimpleUploadedFile("1x1.png",
                                                        image_bytes),
                            is_published = True)
        super().setUpTestData()
        GameDevRole.objects.create(game_id=1, user_id=1, role="Composer")
    
    @classmethod
    def tearDownClass(cls) -> None:
        # print("teardown forms tests")
        # game = Game.objects.get(slug='test3')
        # game.delete()
        shutil.rmtree(settings.test.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()
    
        

    def test_game_form_fields_attrs_class(self):
        form = GameForm()

        self.assertEqual(form.fields['name'].widget.attrs.get("class"), "form-control")
        self.assertEqual(form.fields['tags'].widget.attrs.get("class"), "form-control")
        self.assertEqual(form.fields['slug'].widget.attrs.get("class"), "form-control")
        self.assertEqual(form.fields['description'].widget.attrs.get("class"), "form-control")
        self.assertEqual(form.fields['file'].widget.attrs.get("class"), "form-control")
        self.assertEqual(form.fields['image'].widget.attrs.get("class"), "form-control")
        self.assertEqual(form.fields['video_url'].widget.attrs.get("class"), "form-control")

        self.assertEqual(form.fields['genre'].widget.attrs.get("class"), "form-select")

    def test_comment_form_field_attrs_class(self):
        form = CommentForm()

        self.assertEqual(form.fields['body'].widget.attrs.get("class"), "form-control")

    def test_comment_form_field_label(self):
        form = CommentForm()

        self.assertFalse(form.fields['body'].label)

    def test_rating_form_field_attrs_class(self):
        form = RatingForm()

        self.assertEqual(form.fields['rating'].widget.attrs.get("class"), 'form-control')

    def test_rating_form_field_label(self):
        form = RatingForm()

        self.assertFalse(form.fields['rating'].label)

    def test_rating_form_rating_range(self):
        form = RatingForm()

        self.assertEqual(form.fields['rating'].widget.attrs.get("min"), 1)
        self.assertEqual(form.fields['rating'].widget.attrs.get("max"), 10)

    def test_rating_form_cleandata(self):
        form = RatingForm(data={'rating':11})
        form.is_valid()
        cd = form.cleaned_data

        self.assertEqual(cd['rating'], 10)

    def test_gamedevrole_form_attrs_class(self):
        form = GameDevRoleForm()
        self.assertEqual(form.fields['role'].widget.attrs.get("class"), 'form-control')
        self.assertEqual(form.fields['dev_username'].widget.attrs.get("class"), 'form-control')

    def test_gamedevrole_form_label(self):
        form = GameDevRoleForm()
        self.assertEqual(form.fields['dev_username'].label, "Developer's username")

    def test_gamedevroleform_setting_of_user_from_username(self):
        role = GameDevRole.objects.get(id=1)
        form = GameDevRoleForm({"role": "Composer", "dev_username": role.user.username})
        form.is_valid()
        cd = form.cleaned_data
        self.assertEqual(cd['dev_username'], role.user.username)

    def test_gamedevroleform_cleaning_dev_username(self):
        form = GameDevRoleForm({"role": "Composer", "dev_username": "user1000"})
        
        self.assertFalse(form.is_valid())