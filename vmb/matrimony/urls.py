from django.urls import path

from vmb.matrimony.views import (
    profile_edit,
    index,
    profile_photos_add,
    profile_photo_action,
)

app_name = "matrimony"
urlpatterns = [
    path("", view=index, name="index"),
    path("profile/edit/<slug:section_id>/", view=profile_edit, name="profile-edit"),
    path("profile/photos/add", view=profile_photos_add, name="profile-photos-add"),
    path(
        "profile/photo/<int:photo_id>/<slug:action>/",
        view=profile_photo_action,
        name="profile-photo-action",
    ),
]
