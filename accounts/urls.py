from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('signup/', views.sign_up, name='sign_up'),
    path("updateprofile/", views.profile_update, name='profile_update'),
    path("profile/<slug:username>/", views.profile_details, name='profile_details'),
]
