from django.contrib import admin
from .models import Profile, Invitation

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user']
    raw_id_fields = ['user']

@admin.register(Invitation)
class InvitaionAdmin(admin.ModelAdmin):
    list_display = ['id']