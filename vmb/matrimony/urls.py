from django.urls import path
from . import views

urlpatterns = [
    path("match/<int:id>/response", views.match_response, name="match_response"),
]
