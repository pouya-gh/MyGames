from django.db import models
from django.conf import settings

import uuid

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f'profile of {self.user.username}'
    
class Invitation(models.Model):
    id = models.UUIDField(primary_key=True, 
                          default=uuid.uuid4,
                          help_text='Unique ID')
    invitee_username = models.CharField(max_length=150, blank=True, default='')
    is_used = models.BooleanField(default=False)