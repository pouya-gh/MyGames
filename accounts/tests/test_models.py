from django.test import TestCase
from accounts.models import Profile
from django.contrib.auth.models import User

class TestUserProfileModel(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        User.objects.create(**{'username':"user1", 'password':"123456789)"})
        Profile.objects.create(user_id=1)

    def test_profile_str_method(self):
        profile = Profile.objects.first()

        self.assertEqual(str(profile), f"profile of {profile.user.username}")