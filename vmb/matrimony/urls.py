from django.urls import path
from . import views

from vmb.matrimony.views import (
    profile_edit,
    index,
    profile_photos_add,
    profile_photo_action,
)

app_name = "matrimony"
urlpatterns = [
    path("match/<int:id>/", views.match_details, name="match-details"),
    path("matches/", views.matches, name="matches"),
    path("match/<int:id>/<slug:action>", views.match_action, name="match-action"),
    path("", view=index, name="index"),
    path("profile/edit/<slug:section_id>/", view=profile_edit, name="profile-edit"),
    path("profile/photos/add", view=profile_photos_add, name="profile-photos-add"),
    path(
        "profile/photo/<int:photo_id>/<slug:action>/",
        view=profile_photo_action,
        name="profile-photo-action",
    ),
]
