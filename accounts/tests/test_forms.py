from django.test import TestCase
from accounts.models import Profile
from django.contrib.auth.models import User
from accounts.forms import UserUpdateForm, ProfileForm

class TestUserProfileForm(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        User.objects.create(**{'username':"user1", 'password':"123456789)"})
        Profile.objects.create(user_id=1)

    def test_user_update_form_attrs_classes(self):
        form = UserUpdateForm()
        
        self.assertEqual(form.fields['email'].widget.attrs.get('class'), 'form-control')
        self.assertEqual(form.fields['first_name'].widget.attrs.get('class'), 'form-control')
        self.assertEqual(form.fields['last_name'].widget.attrs.get('class'), 'form-control')

    def test_user_profile_form_attrs_classes(self):
        form = ProfileForm()

        self.assertEqual(form.fields['date_of_birth'].widget.attrs.get('class'), 'form-control')
        self.assertEqual(form.fields['bio'].widget.attrs.get('class'), 'form-control')