from django.urls import path
from . import views

urlpatterns = [
    path("response/<int:id>", views.response, name="response"),
    path("accept_or_reject/<int:id>", views.accept_or_reject, name="accept_or_reject"),
]
