from django.urls import path

from vmb.matrimony.views import (
    profile_edit,
    index,
    profile_details,
    profile_photos_add,
    profile_photo_action,
    matches,
    match_create,
    match_details,
    match_action,
    search,
    mark_as_read,
    mark_all_as_read,
    view_all_notifications,
)

app_name = "matrimony"
urlpatterns = [
    path("", view=index, name="index"),
    path("profile/edit/<slug:section_id>/", view=profile_edit, name="profile-edit"),
    path("profile/photos/add", view=profile_photos_add, name="profile-photos-add"),
    path("profile/<slug:profile_id>/", view=profile_details, name="profile-details"),
    path(
        "profile/photo/<int:photo_id>/<slug:action>/",
        view=profile_photo_action,
        name="profile-photo-action",
    ),
    path("search/", search, name="search"),
    path("matches/", matches, name="matches"),
    path("matches/<slug:category>/", matches, name="matches"),
    path("match/<int:id>", match_details, name="match-details"),
    path("match/<int:id>/<slug:action>", match_action, name="match-action"),
    path("match/<slug:profile_id>/create/", match_create, name="match-create"),
    path("mark_as_read/<int:pk>", mark_as_read, name="mark_as_read"),
    path("mark_all_as_read/", mark_all_as_read, name="mark_all_as_read"),
    path(
        "view_all_notifications/", view_all_notifications, name="view_all_notifications"
    ),
]
