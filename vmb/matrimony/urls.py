from django.urls import path

from vmb.matrimony.views import profile_edit, index

app_name = "matrimony"
urlpatterns = [
    path("", view=index, name="index"),
    path("profile/edit/<slug:section_id>/", view=profile_edit, name="profile-edit"),
]
