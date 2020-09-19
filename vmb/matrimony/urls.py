from django.urls import path

from vmb.matrimony.views import profile_edit, index, profile_photos_ajax

app_name = "matrimony"
urlpatterns = [
    path("", view=index, name="index"),
    path("profile/edit/<slug:section_id>/", view=profile_edit, name="profile-edit"),
    path("ajax/profile/photos", view=profile_photos_ajax, name="profile-photos-ajax"),
]
