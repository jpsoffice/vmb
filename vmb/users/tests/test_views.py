import pytest
from django.conf import settings
from django.test import RequestFactory

from vmb.users.views import UserRedirectView, UserUpdateView

pytestmark = pytest.mark.django_db
from django.urls import reverse
from vmb.users.forms import UserCreationForm
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from vmb.matrimony.models.profiles import *
import datetime
from tos.models import *
from vmb.matrimony.tests.factories import *

class TestUserUpdateView:
    """
    TODO:
        extracting view initialization code as class-scoped fixture
        would be great if only pytest-django supported non-function-scoped
        fixture db access -- this is a work-in-progress for now:
        https://github.com/pytest-dev/pytest-django/pull/258
    """

    def test_get_success_url(
        self, user: settings.AUTH_USER_MODEL, request_factory: RequestFactory
    ):
        view = UserUpdateView()
        request = request_factory.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_success_url() == f"/users/{user.username}/"

    def test_get_object(
        self, user: settings.AUTH_USER_MODEL, request_factory: RequestFactory
    ):
        view = UserUpdateView()
        request = request_factory.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_object() == user


class TestUserRedirectView:
    def test_get_redirect_url(
        self, user: settings.AUTH_USER_MODEL, request_factory: RequestFactory
    ):
        view = UserRedirectView()
        request = request_factory.get("/fake-url")
        request.user = user

        view.request = request

        assert view.get_redirect_url() == f"/users/{user.username}/"

def test_user_signup_view(client):

    data = {
        "email":"test_user@gmail.com",
        "password1":"wordpass123",
        "password2":"wordpass123",
        "name":"test_user",
        "gender":"M",
        "marital_status":"UMR",
        "phone":"9876543210",
        "dob":"Dec 14, 2000",
        "rounds_chanting":20,
        "profile_created_by":"SE",
        "contact_person_name":"test_user123",
    }

    response = client.post('http://127.0.0.1:8000/accounts/signup/', data=data, follow=True)

    assert response.status_code == 200
    assert 'account/verification_sent.html' in (t.name for t in response.templates)


def test_user_login_view(client):

    user = UserCustomFactory()
    profile = MatrimonyFactory(user=user, profile_id=user.username)
    EmailAddress.objects.create(user=profile.user, email=profile.user.email, primary=True, verified=True)
    tos = TermsOfService.objects.create(active=True, content="This is the new TOS.")
    UserAgreement.objects.create(user=profile.user,terms_of_service=tos)
    response = client.post('http://127.0.0.1:8000/accounts/login/', data={'login':profile.user.email, 'password':'wordpass123'}, follow=True)
    
    assert response.status_code == 200
    assert 'matrimony/profile_edit.html' in (t.name for t in response.templates)


