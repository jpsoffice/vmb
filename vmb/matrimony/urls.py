from django.urls import path
from . import views

urlpatterns = [
    path("response/<int:id>", views.response, name="response"),
    path("match/<int:id>", views.match, name="match"),
]
