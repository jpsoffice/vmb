import pytest
from django.conf import settings
from django.test import RequestFactory

from vmb.users.tests.factories import UserFactory

from django.core.management import call_command

import os

@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> settings.AUTH_USER_MODEL:
    return UserFactory()


@pytest.fixture
def request_factory() -> RequestFactory:
    return RequestFactory()

@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        for i in os.listdir('/app/vmb/matrimony/fixtures/'):
            call_command('loaddata', f'/app/vmb/matrimony/fixtures/{i}')
