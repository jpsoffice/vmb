from typing import Any, Sequence

from django.contrib.auth import get_user_model
from factory import Faker, post_generation
import factory

from faker.factory import Factory
Faker = Factory.create
fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):

    username = fake.user_name()
    email = fake.email()
    name = fake.name()

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = fake.password(
            length=42,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True,
        )
        self.set_password(password)

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]

